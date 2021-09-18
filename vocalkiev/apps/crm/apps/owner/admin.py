from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export.results import RowResult
from django.utils.translation import gettext_lazy as _

from vocalkiev.apps.crm.models import *

admin.site.site_header = _("CRM")
admin.site.site_title = _("Owner Dashboard")
admin.site.index_title = _("CRM Owner Dashboard")


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


class SubscriptionResource(ModelResource):
    class Meta:
        model = Subscription
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ['id']
        fields = ('id', 'name', 'price', 'percentage', 'lessons_qty', 'percentage_if_absent', 'created_at', 'updated_at')


class ClientAdmin(ImportExportActionModelAdmin):
    resource_class = ClientResource


class SubscriptionAdmin(ImportExportActionModelAdmin,  admin.ModelAdmin):
    resource_class = SubscriptionResource


admin.site.register(Place)
admin.site.register(Subject)
admin.site.register(LessonComment)
admin.site.register(ClientComment)
admin.site.register(Client, ClientAdmin)
admin.site.register(Classroom)
admin.site.register(ClientSubscription)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Lesson)
admin.site.register(Payment)
