import calendar
from django.utils import timezone

from django import forms
from django.utils.translation import gettext_lazy as _

import vocalkiev.apps.crm.models as models

users = models.User.objects.all()
teachers = users.filter(groups__name='Teacher')


class PlaceDateForm(forms.Form):
    client_subscription = forms.IntegerField(widget=forms.HiddenInput())
    teacher = forms.ModelChoiceField(label=_('Teacher'), queryset=teachers)
    place = forms.ModelChoiceField(label=_('Place'), queryset=models.Place.objects.all())
    date = forms.DateField(label=_('Date'), widget=forms.SelectDateWidget())

    def __init__(self, client_subscription: models.ClientSubscription, data=None, *args, **kwargs):
        super(PlaceDateForm, self).__init__(data, *args, **kwargs)

        self.fields['client_subscription'].initial = client_subscription.pk
        self.fields['date'].initial = timezone.now().date()
        self.fields['teacher'].initial = client_subscription.teacher


class TimeForm(forms.Form):
    client_subscription = forms.IntegerField(widget=forms.HiddenInput())
    teacher = forms.IntegerField(widget=forms.HiddenInput())
    place = forms.IntegerField(widget=forms.HiddenInput())
    date_day = forms.IntegerField(widget=forms.HiddenInput())
    date_month = forms.IntegerField(widget=forms.HiddenInput())
    date_year = forms.IntegerField(widget=forms.HiddenInput())
    date_hour = forms.ChoiceField(label=_('Time'), required=False)

    def __init__(self,
                 client_subscription: models.ClientSubscription, teacher: models.User,
                 data=None, *args, **kwargs):
        super(TimeForm, self).__init__(data, *args, **kwargs)

        self.fields['client_subscription'].initial = client_subscription.pk
        self.fields['teacher'].initial = teacher.pk

        classrooms = models.Classroom.objects.filter(place_id=int(data['place']))

        choices = []
        for hour in range(9, 22):
            for classroom in classrooms:
                dt = timezone.datetime(int(data['date_year']), int(data['date_month']), int(data['date_day']), hour)
                if models.Lesson.can_create(classroom, dt, teacher, client_subscription.client):
                    choices.append((hour, f"{hour}:00"))
                    break
        self.fields['date_hour'].choices = choices


class ClassroomForm(forms.Form):
    client_subscription = forms.IntegerField(widget=forms.HiddenInput())
    teacher = forms.IntegerField(widget=forms.HiddenInput())
    place = forms.IntegerField(widget=forms.HiddenInput())
    date_day = forms.IntegerField(widget=forms.HiddenInput())
    date_month = forms.IntegerField(widget=forms.HiddenInput())
    date_year = forms.IntegerField(widget=forms.HiddenInput())
    date_hour = forms.IntegerField(widget=forms.HiddenInput())
    classroom = forms.ChoiceField(label=_('Classroom'), required=False)

    def __init__(self,
                 client_subscription: models.ClientSubscription, teacher: models.User,
                 data=None, *args, **kwargs):
        super(ClassroomForm, self).__init__(data, *args, **kwargs)

        self.fields['client_subscription'].initial = client_subscription.pk
        self.fields['teacher'].initial = teacher.pk

        classrooms = models.Classroom.objects.filter(place_id=int(data['place']))

        choices = []
        for classroom in classrooms:
            dt = timezone.datetime(int(data['date_year']), int(data['date_month']), int(data['date_day']),
                                   int(data['date_hour']))
            if models.Lesson.can_create(classroom, dt, teacher, client_subscription.client):
                choices.append((classroom.id, str(classroom)))
        self.fields['classroom'].choices = choices


class PassLessonForm(forms.Form):
    comment = forms.CharField(label=_('Comment'), widget=forms.TextInput(attrs={'placeholder': _('Comment')}),
                              required=False)
    was_absent = forms.BooleanField(label=_('Was absent'), initial=False, required=False)


class LessonReportsForm(forms.Form):
    month_half = forms.ChoiceField(label=_('Month half'), initial=1)
    month = forms.ChoiceField(label=_('Month'), initial=timezone.now().month)
    year = forms.ChoiceField(label=_('Year'), initial=timezone.now().year)

    def __init__(self, data=None, *args, **kwargs):
        super(LessonReportsForm, self).__init__(data, *args, **kwargs)

        today = timezone.now().today()

        years = []
        for y in range(today.year - 1, today.year + 2):
            years.append((y, y,))
        self.fields['year'].choices = years
        self.fields['year'].initial = today.year

        months = []
        for mi, m in enumerate(calendar.month_name):
            if m:
                months.append((mi, _(m)))
        self.fields['month'].choices = months
        self.fields['month'].initial = today.month

        month_halves = [
            (1, _('First half (1-15)')),
            (2, _('Second half (16-end)'))
        ]
        self.fields['month_half'].choices = month_halves
        self.fields['month_half'].initial = 1


class ClientForm(forms.Form):
    first_name = forms.CharField(label=_('First name'), max_length=64)
    last_name = forms.CharField(label=_('Last name'), required=False, max_length=64)
    email = forms.CharField(label=_('Email'), required=False)
    phone = forms.CharField(label=_('Phone'), required=False, max_length=20)
    client_comment = forms.CharField(label=_('Client Comment'), required=False)

    field_order = ['first_name', 'last_name', 'email', 'phone', 'client_comment']


class ClientCommentForm(forms.Form):
    comment = forms.CharField(label=_('Client Comment'))


class ClientSubscriptionForm(forms.Form):
    subscription = forms.ModelChoiceField(label=_('Subscription'), queryset=models.Subscription.objects.exclude(pk__in=[2, 3]))
    client = forms.ModelChoiceField(label=_('Client'), queryset=models.Client.objects.all())
    teacher = forms.ModelChoiceField(label=_('Teacher'), queryset=teachers.exclude(username = 'rent'))
    payment_type = forms.ChoiceField(label=_('Payment type'), choices=models.PaymentType.choices)
    comment = forms.CharField(label=_('Comment'), widget=forms.TextInput(attrs={'placeholder': _('Comment')}),
                              required=False)

    def __init__(self, data=None, *args, **kwargs):
        super(ClientSubscriptionForm, self).__init__(data, *args, **kwargs)

        self.fields['payment_type'].initial = models.PaymentType.CASH


class RentSubscriptionForm(forms.Form):
    subscription = forms.ModelChoiceField(label=_('Subscription'), queryset=models.Subscription.objects.filter(pk__in=[2, 3]))
    client = forms.ModelChoiceField(label=_('Client'), queryset=models.Client.objects.all())
    teacher = forms.ModelChoiceField(label=_('Teacher'), queryset=teachers.filter(username='rent'), empty_label=None)
    payment_type = forms.ChoiceField(label=_('Payment type'), choices=models.PaymentType.choices)
    comment = forms.CharField(label=_('Comment'), widget=forms.TextInput(attrs={'placeholder': _('Comment')}),
                              required=False)

    def __init__(self, data=None, *args, **kwargs):
        super(RentSubscriptionForm, self).__init__(data, *args, **kwargs)

        self.fields['payment_type'].initial = models.PaymentType.CASH
