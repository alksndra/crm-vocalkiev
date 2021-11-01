from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from vocalkiev.apps.crm import models
import nested_admin

from vocalkiev.forms import BaseForm


class AdministratorAdminSite(admin.AdminSite):
    site_header = _("CRM")
    site_title = _("Administrator Dashboard")
    index_title = _("CRM Administrator Dashboard")


class EmptyInline(nested_admin.NestedStackedInline):
    initial_num = 0
    extra = 0
    min_num = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ClientCommentInline(EmptyInline):
    model = models.ClientComment
    fk_name = 'client'
    exclude = ('creator', 'status',)


class PaymentInline(EmptyInline):
    model = models.Payment
    fk_name = 'client_subscription'
    exclude = ('creator', 'status',)


class LessonCommentInline(EmptyInline):
    model = models.LessonComment
    fk_name = 'lesson'
    exclude = ('creator', 'status',)


class LessonInline(EmptyInline):
    model = models.Lesson
    fk_name = 'client_subscription'
    exclude = ('creator', 'status', 'teacher', 'classroom', 'datetime',)
    inlines = [LessonCommentInline]

    def has_add_permission(self, request, obj=None):
        return False


class ClientSubscriptionInline(EmptyInline):
    model = models.ClientSubscription
    fk_name = 'client'
    initial_num = 0
    extra = 0
    min_num = 0
    exclude = ('creator', 'status',)
    inlines = [
        LessonInline,
        # PaymentInline,
    ]

    def get_field_queryset(self, db, db_field, request):
        qs = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'teacher':
            qs = models.User.objects.filter(groups__name='Teacher')
        return qs


class ClientAdmin(BaseForm, nested_admin.NestedModelAdmin):
    inlines = [
        ClientCommentInline,
        ClientSubscriptionInline
    ]

    class Media:
        css = {
            "all": ('crm/administrator/style.css',)
        }
        js = ('js/jquery-3.5.1.slim.min.js', 'crm/administrator/script.js',)


administrator_admin_site = AdministratorAdminSite(name='administrator')

administrator_admin_site.register(models.Client, ClientAdmin)
