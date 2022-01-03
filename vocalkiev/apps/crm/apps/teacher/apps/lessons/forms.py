import calendar
from django.utils import timezone

from django import forms
from django.utils.translation import gettext_lazy as _

from vocalkiev.apps.crm.models import Place, Lesson, Classroom, User, ClientSubscription

teachers = User.objects.filter(groups__name='Teacher')


class PlaceDateForm(forms.Form):
    client_subscription = forms.IntegerField(widget=forms.HiddenInput())
    teacher = forms.ModelChoiceField(label=_('Teacher'), queryset=teachers)
    place = forms.ModelChoiceField(label=_('Place'), queryset=Place.objects.all())
    date = forms.DateField(label=_('Date'), widget=forms.SelectDateWidget())

    def __init__(self, client_subscription: ClientSubscription, data=None, *args, **kwargs):
        super(PlaceDateForm, self).__init__(data, *args, **kwargs)

        self.fields['client_subscription'].initial = client_subscription.id
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

    def __init__(self, client_subscription: ClientSubscription, teacher: User, data=None, *args, **kwargs):
        super(TimeForm, self).__init__(data, *args, **kwargs)

        self.fields['client_subscription'].initial = client_subscription.id
        self.fields['teacher'].initial = teacher.id

        classrooms = Classroom.objects.filter(place_id=int(data['place']))

        choices = []
        for hour in range(9, 22):
            for classroom in classrooms:
                dt = timezone.datetime(int(data['date_year']), int(data['date_month']), int(data['date_day']), hour)
                if Lesson.can_create(classroom, dt, teacher, client_subscription.client):
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

    def __init__(self, client_subscription: ClientSubscription, teacher: User, data=None, *args, **kwargs):
        super(ClassroomForm, self).__init__(data, *args, **kwargs)

        self.fields['client_subscription'].initial = client_subscription.id
        self.fields['teacher'].initial = teacher.id

        classrooms = Classroom.objects.filter(place_id=int(data['place']))

        choices = []
        for classroom in classrooms:
            dt = timezone.datetime(int(data['date_year']), int(data['date_month']), int(data['date_day']), int(data['date_hour']))
            if Lesson.can_create(classroom, dt, teacher, client_subscription.client):
                choices.append((classroom.id, str(classroom)))
        self.fields['classroom'].choices = choices


class PassLessonForm(forms.Form):
    comment = forms.CharField(label=_('Comment'), widget=forms.TextInput(attrs={'placeholder': _('Comment')}), required=False)
    was_absent = forms.BooleanField(label=_('Was absent'), initial=False, required=False)


class LessonReportsForm(forms.Form):
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
