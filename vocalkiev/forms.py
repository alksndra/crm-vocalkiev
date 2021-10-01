from django.utils.translation import gettext_lazy as _


def translate_base_fields(form):
    for field in form.base_fields:
        form.base_fields[field].label = _(form.base_fields[field].label)
    return form


class BaseForm:
    exclude = ('creator',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return translate_base_fields(form)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            for instance in formset.save(commit=False):
                if not instance.pk:
                    instance.creator = request.user
                instance.save()
