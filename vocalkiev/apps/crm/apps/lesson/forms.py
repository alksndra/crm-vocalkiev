import calendar
from datetime import datetime

from django import forms
from django.utils.translation import gettext_lazy as _

from vocalkiev.apps.crm.models import Place, Lesson, Classroom


class PlaceDateForm(forms.Form):
    place = forms.ModelChoiceField(label=_('Place'), queryset=Place.objects.all())
    date = forms.DateField(label=_('Date'), widget=forms.SelectDateWidget())


class TimeForm(forms.Form):
    place = forms.IntegerField(widget=forms.HiddenInput())
    date_day = forms.IntegerField(widget=forms.HiddenInput())
    date_month = forms.IntegerField(widget=forms.HiddenInput())
    date_year = forms.IntegerField(widget=forms.HiddenInput())
    date_hour = forms.ChoiceField(label=_('Time'), required=False)

    def __init__(self, data=None, *args, **kwargs):
        super(TimeForm, self).__init__(data, *args, **kwargs)

        classrooms_qty = Classroom.objects.filter(place_id=int(data['place'])).count()

        choices = []
        for hour in range(9, 22):
            lessons_qty = Lesson.objects.filter(
                classroom__place_id=int(data['place']),
                datetime__year=int(data['date_year']),
                datetime__month=int(data['date_month']),
                datetime__day=int(data['date_day']),
                datetime__hour=hour,
            ).count()

            if lessons_qty < classrooms_qty:
                choices.append((hour, f"{hour}:00"))
        self.fields['date_hour'].choices = choices


class ClassroomForm(forms.Form):
    place = forms.IntegerField(widget=forms.HiddenInput())
    date_day = forms.IntegerField(widget=forms.HiddenInput())
    date_month = forms.IntegerField(widget=forms.HiddenInput())
    date_year = forms.IntegerField(widget=forms.HiddenInput())
    date_hour = forms.IntegerField(widget=forms.HiddenInput())
    classroom = forms.ChoiceField(label=_('Classroom'), required=False)

    def __init__(self, data=None, *args, **kwargs):
        super(ClassroomForm, self).__init__(data, *args, **kwargs)

        classrooms = Classroom.objects.filter(place_id=int(data['place']))

        choices = []
        for cr in classrooms:
            lessons_qty = Lesson.objects.filter(
                classroom_id=cr.id,
                datetime__year=int(data['date_year']),
                datetime__month=int(data['date_month']),
                datetime__day=int(data['date_day']),
                datetime__hour=int(data['date_hour']),
            ).count()

            if lessons_qty == 0:
                choices.append((cr.id, str(cr)))
        self.fields['classroom'].choices = choices


class PassLessonForm(forms.Form):
    comment = forms.CharField(label=_('Comment'), widget=forms.TextInput(attrs={'placeholder': _('Comment')}))


class LessonReportsForm(forms.Form):
    month = forms.ChoiceField(label=_('Month'), initial=datetime.today().month)
    year = forms.ChoiceField(label=_('Year'), initial=datetime.today().year)

    def __init__(self, data=None, *args, **kwargs):
        super(LessonReportsForm, self).__init__(data, *args, **kwargs)

        today = datetime.today()

        years = []
        for y in range(today.year - 1, today.year + 2):
            years.append((y, y,))
        self.fields['year'].choices = years

        months = []
        for mi, m in enumerate(calendar.month_name):
            if m:
                months.append((mi, _(m)))
        self.fields['month'].choices = months
