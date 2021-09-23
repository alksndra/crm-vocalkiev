from django.contrib import admin
from vocalkiev.apps.crm.models import *
from django.utils.translation import gettext_lazy as _
from .forms import *
from django.utils import timezone


class TeacherAdminSite(admin.AdminSite):
    site_header = _("CRM")
    site_title = _("Teacher Dashboard")
    index_title = _("CRM Teacher Dashboard")


class LessonCommentInline(admin.StackedInline):
    model = LessonComment
    exclude = ('user',)


class LessonInline(admin.StackedInline):
    model = Lesson
    exclude = ('teacher',)
    initial_num = 1
    extra = 0
    min_num = 1


class LessonCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'comment')
    search_fields = ('lesson',)

    def get_changeform_initial_data(self, request):
        return {'user': request.user.pk}

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_module_permission(self, request):
        return False


class ClientSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'client', 'teacher', 'status', 'comment', 'payment_type', 'created_at', 'updated_at')
    search_fields = ('subscription', 'client', 'teacher', 'status',)
    readonly_fields = ['subscription', 'client', 'teacher', 'status', 'comment', 'payment_type', ]
    inlines = [
        LessonInline,
    ]

    def get_queryset(self, request):
        qs = super(ClientSubscriptionAdmin, self).get_queryset(request)
        return qs.filter(teacher=request.user)

    def get_field_queryset(self, db, db_field, request):
        qs = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'teacher':
            qs = ClientSubscription.objects.filter(teacher=request.user)
        return qs

    def save_formset(self, request, form, formset, change):
        for form_ in formset.forms:
            obj = form_.save(commit=False)
            if not obj.pk:
                obj.teacher = request.user
            obj.save()
        formset.save()


class LessonAdmin(admin.ModelAdmin):
    list_display = ('client_subscription', 'teacher', 'classroom', 'datetime', 'status')
    search_fields = ('client_subscription', 'teacher')
    form = LessonAdminForm
    inlines = [
        LessonCommentInline,
    ]

    def get_queryset(self, request):
        qs = super(LessonAdmin, self).get_queryset(request)
        return qs.filter(teacher=request.user)

    def get_field_queryset(self, db, db_field, request):
        qs = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'client_subscription':
            qs = ClientSubscription.objects.filter(teacher=request.user)
        return qs

    def save_formset(self, request, form, formset, change):
        for form_ in formset.forms:
            obj = form_.save(commit=False)
            if not obj.pk:
                obj.user = request.user
            obj.save()
        formset.save()

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.datetime < timezone.now():
            return 'client_subscription', 'classroom', 'datetime', 'status'
        return super().get_readonly_fields(request, obj)


teacher_admin_site = TeacherAdminSite(name='teacher')

teacher_admin_site.register(LessonComment, LessonCommentAdmin)
teacher_admin_site.register(ClientSubscription, ClientSubscriptionAdmin)
teacher_admin_site.register(Lesson, LessonAdmin)
