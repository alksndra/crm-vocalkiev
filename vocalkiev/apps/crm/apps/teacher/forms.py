from django import forms
from vocalkiev.apps.crm.models import *


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].widget = forms.HiddenInput()
        self.fields['teacher'].required = False

    def clean(self):
        data = self.cleaned_data
        if not data.get('teacher'):
            data['teacher'] = data['client_subscription'].teacher
        return data


