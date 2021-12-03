import calendar
from django.utils import timezone

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.template import loader

from vocalkiev.apps.crm.models import Place, Classroom, Lesson


def index(request):
    today = timezone.now()
    return redirect('crm-schedule-day', year=today.year, month=today.month, day=today.day)


def schedule_day(request, year=2021, month=0, day=0, place_id=0):
    places = Place.objects.all()
    calendar.setfirstweekday(calendar.MONDAY)
    try:
        monthdays = calendar.Calendar().monthdayscalendar(year, month)
    except calendar.IllegalMonthError:
        monthdays = []

    years = []
    for y in range(timezone.now().year, timezone.now().today().year + 3):
        years.append(y)

    months = []
    for m in calendar.month_name:
        if m:
            months.append(m)

    weekdays = []
    for wd in monthdays:
        for di, d in enumerate(wd):
            if d > 0:
                weekdays.append(list(calendar.day_name)[di])

    place = places.filter(id=place_id).first()
    classrooms = Classroom.objects.filter(place_id=place.id) if place else []

    data = []

    if year and month and day:
        lessons = Lesson.objects.filter(datetime__year=year, datetime__month=month, datetime__day=day)
        for t in range(9, 22):
            row = {'time': str(t) + ':00'}
            for lesson in lessons.filter(datetime__hour=t):
                row['dcr_' + str(lesson.classroom.id) + '_t'] = lesson.teacher.get_full_name()
                row['dcr_' + str(lesson.classroom.id) + '_c'] = lesson.client_subscription.client.__str__()
            data.append(row)

    template = loader.get_template('schedule/day.html')
    context = {
        'places': places,
        'year': year,
        'month': month,
        'month_name': months[month - 1] if month else '',
        'day': day,
        'place': place_id,
        'place_name': place.name if place else '',
        'monthdays': monthdays,
        'months': months,
        'years': years,
        'weekdays': weekdays,
        'classrooms': classrooms,
        'data': data
    }

    return HttpResponse(template.render(context, request))


def schedule(request, year=2021, month=1):
    places = Place.objects.all()
    classrooms = Classroom.objects.all()

    calendar.setfirstweekday(calendar.MONDAY)
    monthdays = calendar.Calendar().monthdayscalendar(year, month)
    data = []
    month_lessons = Lesson.objects.filter(datetime__year=year, datetime__month=month)
    for d in range(0, len(monthdays)):
        week_lessons = {}
        time = {
            'time': _('Date')
        }
        for imd, md in enumerate(monthdays[d]):
            if md > 0:
                time['d_' + str(imd + 1)] = md
                week_lessons[md] = month_lessons.filter(datetime__day=md)

        data.append(time)

        for t in range(9, 22):
            row = {
                'time': str(t) + ':00'
            }
            for imd, md in enumerate(monthdays[d]):
                if md > 0:
                    for l in week_lessons[md].filter(datetime__hour=t):
                        cs = l.client_subscription
                        row[get_dp(imd, l) + '_t'] = l.teacher.get_full_name()
                        row[get_dp(imd, l) + '_c'] = cs.client.get_full_name()
            data.append(row)

    months = []
    for m in calendar.month_name:
        if m:
            months.append(m)

    years = []
    for y in range(timezone.now().today().year, timezone.now().today().year + 3):
        years.append(y)

    template = loader.get_template('schedule/index.html')
    context = {
        'year': year,
        'month': month,
        'month_name': months[month - 1],
        'weekDays': calendar.day_name,
        'months': months,
        'years': years,
        'places': places,
        'classrooms': classrooms,
        'data': data
    }

    return HttpResponse(template.render(context, request))


def get_dp(imd: int, lesson: Lesson):
    cr = lesson.classroom
    p = cr.place
    return 'dp_' + str(imd + 1) + '_' + str(p.id) + '_' + str(cr.id)
