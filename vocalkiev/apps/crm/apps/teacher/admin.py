from django.contrib import admin
from vocalkiev.apps.crm.models import *
from django.utils.translation import gettext_lazy as _
from .forms import *


class TeacherAdminSite(admin.AdminSite):
    site_header = _("CRM")
    site_title = _("Teacher Dashboard")
    index_title = _("CRM Teacher Dashboard")


class LessonCommentInline(admin.StackedInline):
    model = LessonComment


class LessonInline(admin.StackedInline):
    model = Lesson


class LessonCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'comment')
    search_fields = ('lesson',)
    form = LessonCommentAdminForm

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
    inlines = [
        LessonInline,
    ]


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


teacher_admin_site = TeacherAdminSite(name='teacher')

teacher_admin_site.register(LessonComment, LessonCommentAdmin)
teacher_admin_site.register(ClientSubscription, ClientSubscriptionAdmin)
teacher_admin_site.register(Lesson, LessonAdmin)
