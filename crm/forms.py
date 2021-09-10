from django import forms
from .models import *


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].required = False
        self.fields['teacher'].help_text = 'Если не ввести имя преподавателя, будет введен преподаватель указанного абонемента'

    def clean(self):
        data = self.cleaned_data
        if not data.get('teacher'):
            data['teacher'] = data['client_subscription'].teacher
        return data


class PaymentAdminForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].help_text = 'Оплата за указанный абонемент'

    def clean(self):
        data = self.cleaned_data
        if not data.get('amount'):
            data['amount'] = data['client_subscription'].subscription.price
        return data



