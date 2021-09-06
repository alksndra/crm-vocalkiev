from django import forms
from .models import *


class ClientForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=UserFullName.objects.all())

    class Meta:
        model = ClientSubscription
