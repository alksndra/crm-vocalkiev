from django import forms
from .models import *


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].required = False
        self.fields['teacher'].help_text = 'sdfsdf'

    def clean(self):
        data = self.cleaned_data
        if not data.get('teacher'):
            data['teacher'] = data['client_subscription'].teacher
        return data
