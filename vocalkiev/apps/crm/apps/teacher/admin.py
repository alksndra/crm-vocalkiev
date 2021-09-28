from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import nested_admin
from vocalkiev.apps.crm.models import LessonComment, Lesson, ClientSubscription
from django.db import models
from django.forms import Textarea, HiddenInput


class TeacherAdminSite(admin.AdminSite):
    site_header = _("CRM")
    site_title = _("Teacher Dashboard")
    index_title = _("CRM Teacher Dashboard")


class LessonCommentInline(nested_admin.NestedStackedInline):
    model = LessonComment
    fk_name = 'lesson'
    exclude = ('user',)
    initial_num = 0
    extra = 0
    min_num = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2})},
    }

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class LessonInline(nested_admin.NestedStackedInline):
    model = Lesson
    fk_name = 'client_subscription'
    exclude = ('teacher', 'status',)
    initial_num = 1
    extra = 0
    min_num = 1
    inlines = [LessonCommentInline]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ClientSubscriptionAdmin(nested_admin.NestedModelAdmin):
    list_display = ('subscription', 'client', 'teacher', 'status', 'comment', 'payment_type', 'created_at', 'updated_at')
    search_fields = ('subscription', 'client', 'teacher', 'status',)
    readonly_fields = ['subscription', 'client', 'teacher', 'status', 'comment', 'payment_type', ]
    inlines = [
        LessonInline,
    ]

    def get_queryset(self, request):
        qs = super(ClientSubscriptionAdmin, self).get_queryset(request)
        return qs.filter(teacher=request.user)

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            if formset.model == Lesson:
                lessons = formset.save(commit=False)
                for lesson in lessons:
                    if not lesson.pk:
                        lesson.teacher = request.user
                    lesson.save()

            if formset.model == LessonComment:
                comments = formset.save(commit=False)
                for comment in comments:
                    if not comment.pk:
                        comment.user = request.user
                    comment.save()


teacher_admin_site = TeacherAdminSite(name='teacher')

teacher_admin_site.register(ClientSubscription, ClientSubscriptionAdmin)
