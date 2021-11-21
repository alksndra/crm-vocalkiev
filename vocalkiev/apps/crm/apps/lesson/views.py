import datetime

from django.shortcuts import render, get_object_or_404, redirect

from vocalkiev.apps.crm.apps.lesson.forms import PlaceDateForm, TimeForm, ClassroomForm
from vocalkiev.apps.crm.models import ClientSubscription, Lesson, Classroom


def index(request):
    client_subscriptions = ClientSubscription.objects.filter(teacher_id=request.user.id)
    return render(request, 'lesson/subscriptions.html', {'client_subscriptions': client_subscriptions})


def lesson(request, client_subscription_id):
    client_subscription = get_object_or_404(ClientSubscription, pk=client_subscription_id)
    place = None
    date = None
    date_hour = None
    time_form = None
    classroom_form = None

    if request.method == 'POST':
        place_date_form = PlaceDateForm(request.POST)
        if place_date_form.is_valid():
            place = place_date_form.cleaned_data['place']
            date = place_date_form.cleaned_data['date']

            time_form = TimeForm(request.POST)
            if time_form.is_valid():
                date_hour = time_form.cleaned_data['date_hour']

                if date_hour:
                    classroom_form = ClassroomForm(request.POST)

                    if classroom_form.is_valid():
                        date_hour = classroom_form.cleaned_data['date_hour']
                        classroom_id = classroom_form.cleaned_data['classroom']

                        if classroom_id:
                            classroom = get_object_or_404(Classroom, pk=classroom_id)

                            dt = datetime.datetime(date.year, date.month, date.day, date_hour)

                            new_lesson = Lesson.objects.create(
                                creator=request.user,
                                client_subscription=client_subscription,
                                classroom=classroom,
                                teacher=request.user,
                                datetime=dt,
                            )
                            new_lesson.save()

                            return redirect('crm-schedule-day',
                                            year=date.year,
                                            month=date.month,
                                            day=date.day,
                                            place_id=classroom.place.id
                                            )
    else:
        place_date_form = PlaceDateForm()

    return render(
        request,
        'lesson/index.html',
        {
            'client_subscription': client_subscription,
            'place': place,
            'date': date,
            'date_hour': date_hour,
            'place_date_form': place_date_form,
            'time_form': time_form,
            'classroom_form': classroom_form,
        }
    )
