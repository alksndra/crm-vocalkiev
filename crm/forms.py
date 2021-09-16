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


class PaymentAdminShortForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('client_subscription',)
        widgets = {
            'client_subscription_id': forms.Select(attrs={'onchange': 'this.form.submit();'})
        }


class PaymentAdminForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = 'admin',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].help_text = 'Оплата за указанный абонемент'

    """def clean(self):
        data = self.cleaned_data
        if not data.get('amount'):
            data['amount'] = data['client_subscription'].subscription.price
        return data"""


class ClientCommentAdminForm(forms.ModelForm):
    class Meta:
        model = ClientComment
        exclude = 'user',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




