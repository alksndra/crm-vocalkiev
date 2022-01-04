from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export.results import RowResult
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from vocalkiev.apps.crm.models import *
from vocalkiev.forms import BaseForm


class OwnerAdminSite(admin.AdminSite):
    site_header = _("CRM")
    site_title = _("Owner Dashboard")
    index_title = _("CRM Owner Dashboard")


class ModelResource(resources.ModelResource):
    def import_row(self, row, instance_loader, **kwargs):
        import_result = super(ModelResource, self).import_row(row, instance_loader, **kwargs)

        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            import_result.diff = [row[val] for val in row]
            import_result.diff.append('Errors: {}'.format([err.error for err in import_result.errors]))
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP

        return import_result


class ClientResource(ModelResource):
    class Meta:
        model = Client
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ['id']
        fields = ('id', 'firstname', 'lastname', 'email', 'phone', ' created_at', 'updated_at')


class ClientAdmin(BaseForm, ImportExportActionModelAdmin):
    resource_class = ClientResource


owner_admin_site = OwnerAdminSite(name='owner')

owner_admin_site.register(Place)
owner_admin_site.register(Subject)
owner_admin_site.register(LessonComment)
owner_admin_site.register(ClientComment)
owner_admin_site.register(Client, ClientAdmin)
owner_admin_site.register(Classroom)
owner_admin_site.register(ClientSubscription)
owner_admin_site.register(Subscription)
owner_admin_site.register(Lesson)
owner_admin_site.register(Payment)
owner_admin_site.register(User, UserAdmin)
owner_admin_site.register(Group)
