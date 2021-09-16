from django import forms
from .models import *


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        exclude = 'teacher',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        if not data.get('teacher'):
            data['teacher'] = data['client_subscription'].teacher
        return data


class PaymentAdminForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = 'admin',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].help_text = 'Оплата за указанный абонемент'


class ClientCommentAdminForm(forms.ModelForm):
    class Meta:
        model = ClientComment
        exclude = 'user',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
