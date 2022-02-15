import datetime

from django.shortcuts import render, get_object_or_404, redirect, resolve_url

from vocalkiev.apps.crm.apps.lessons.forms import PlaceDateForm, TimeForm, ClassroomForm, PassLessonForm, \
    LessonReportsForm, ClientSubscriptionForm, ClientForm, ClientCommentForm
from vocalkiev.apps.crm.models import ClientSubscription, Lesson, Classroom, LessonComment, User, Client, Status, \
    ClientComment
from vocalkiev.apps.crm.apps.lessons.helpers import is_before_today


def index(request):
    return redirect('crm-subscriptions')


def show_subscriptions(request):
    if request.user.groups.filter(name='Administrator').exists():
        client_subscriptions = ClientSubscription.objects.filter(status=Status.ACTIVE)
    else:
        client_subscriptions = ClientSubscription.objects.filter(status=Status.ACTIVE, teacher_id=request.user.id)

    return render(
        request,
        'lessons/subscriptions.html',
        {
            'client_subscriptions': client_subscriptions
        }
    )


def show_lessons(request, client_subscription_id):
    client_subscription = ClientSubscription.objects.get(pk=client_subscription_id)
    lessons = Lesson.objects.filter(client_subscription__id=client_subscription.id)

    if request.method == 'POST':
        client_comment_form = ClientCommentForm(request.POST)

        if client_comment_form.is_valid():
            comment = client_comment_form.cleaned_data['comment']

            new_client_comment = ClientComment.objects.create(
                creator=request.user,
                client=client_subscription.client,
                comment=comment,
            )

            return redirect('crm-subscription-lessons', client_subscription_id=client_subscription.id)
    else:
        client_comment_form = ClientCommentForm()

    return render(
        request,
        'lessons/lessons.html',
        {
            'client_subscription': client_subscription,
            'lessons': lessons,
            'client_comment_form': client_comment_form,
        }
    )


def create_lesson(request, client_subscription_id):
    client_subscription = get_object_or_404(ClientSubscription, pk=client_subscription_id)

    if not client_subscription.can_create_lesson():
        return redirect('crm-subscription-lessons', client_subscription_id=client_subscription.id)

    place = None
    date = None
    date_hour = None
    time_form = None
    classroom_form = None

    if request.method == 'POST':
        place_date_form = PlaceDateForm(client_subscription, data=request.POST)
        if place_date_form.is_valid():
            teacher = place_date_form.cleaned_data['teacher']
            place = place_date_form.cleaned_data['place']
            date = place_date_form.cleaned_data['date']

            if is_before_today(date.year, date.month, date.day):
                return redirect('crm-create-lesson', client_subscription_id=client_subscription.id)

            time_form = TimeForm(client_subscription, teacher, request.POST)
            if time_form.is_valid():
                date_hour = time_form.cleaned_data['date_hour']

                if date_hour:
                    classroom_form = ClassroomForm(client_subscription, teacher, request.POST)

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
                                teacher=teacher,
                                datetime=dt,
                            )

                            new_lesson.save()

                            return redirect('crm-schedule-day-place',
                                            year=date.year,
                                            month=date.month,
                                            day=date.day,
                                            place_id=classroom.place.id
                                            )
    else:
        place_date_form = PlaceDateForm(client_subscription)

    return render(
        request,
        'lessons/create-lesson.html',
        {
            'form_action': resolve_url('crm-create-lesson', client_subscription_id=client_subscription_id),
            'client_subscription': client_subscription,
            'place': place,
            'date': date,
            'date_hour': date_hour,
            'place_date_form': place_date_form,
            'time_form': time_form,
            'classroom_form': classroom_form,
        }
    )


def update_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    client_subscription = lesson.client_subscription

    if lesson.teacher != request.user:
        return redirect('crm-subscription-lessons', client_subscription_id=client_subscription.id)

    if (request.user.groups.filter(name='Administrator').exists() and lesson.can_update_by_administrator())\
            or not lesson.can_update_by_teacher():
        return redirect('crm-subscription-lessons', client_subscription_id=client_subscription.id)

    place = lesson.classroom.place
    date = lesson.datetime
    date_hour = lesson.datetime.hour
    time_form = None
    classroom_form = None

    if request.method == 'POST':
        place_date_form = PlaceDateForm(client_subscription, data=request.POST)
        if place_date_form.is_valid():
            teacher = place_date_form.cleaned_data['teacher']
            place = place_date_form.cleaned_data['place']
            date = place_date_form.cleaned_data['date']

            time_form = TimeForm(client_subscription, teacher, request.POST)
            if time_form.is_valid():
                date_hour = time_form.cleaned_data['date_hour']

                if date_hour:
                    classroom_form = ClassroomForm(client_subscription, teacher, request.POST)

                    if classroom_form.is_valid():
                        date_hour = classroom_form.cleaned_data['date_hour']
                        classroom_id = classroom_form.cleaned_data['classroom']

                        if classroom_id:
                            classroom = get_object_or_404(Classroom, pk=classroom_id)

                            dt = datetime.datetime(date.year, date.month, date.day, date_hour)

                            lesson.classroom = classroom
                            lesson.teacher = teacher
                            lesson.datetime = dt

                            lesson.save()

                            return redirect('crm-schedule-day-place',
                                            year=date.year,
                                            month=date.month,
                                            day=date.day,
                                            place_id=classroom.place.id
                                            )
    else:
        place_date_form = PlaceDateForm(client_subscription)

    return render(
        request,
        'lessons/update-lesson.html',
        {
            'form_action': resolve_url('crm-update-lesson', lesson_id=lesson_id),
            'lesson': lesson,
            'client_subscription': client_subscription,
            'place': place,
            'date': date,
            'date_hour': date_hour,
            'place_date_form': place_date_form,
            'time_form': time_form,
            'classroom_form': classroom_form,
        }
    )


def pass_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)

    if not lesson.can_pass():
        return redirect('crm-subscription-lessons', client_subscription_id=lesson.client_subscription.id)

    if request.method == 'POST':
        pass_lesson_form = PassLessonForm(request.POST)
        if pass_lesson_form.is_valid():
            was_absent = pass_lesson_form.cleaned_data['was_absent']

            lesson.is_passed = True
            lesson.was_absent = was_absent
            lesson.save()

            if pass_lesson_form.cleaned_data.get('comment'):
                new_comment = LessonComment.objects.create(
                    creator=request.user,
                    lesson=lesson,
                    comment=pass_lesson_form.cleaned_data['comment']
                )
                new_comment.save()

            return redirect('crm-subscription-lessons', client_subscription_id=lesson.client_subscription.id)
    else:
        pass_lesson_form = PassLessonForm()

    return render(
        request,
        'lessons/pass-lesson.html',
        {
            'lesson': lesson,
            'form': pass_lesson_form
        }
    )


def reports(request):
    lessons = None
    year = None
    month = None
    total = 0

    if request.method == 'POST':
        lesson_reports_form = LessonReportsForm(request.POST)

        if lesson_reports_form.is_valid():
            year = int(lesson_reports_form.cleaned_data['year'])
            month = int(lesson_reports_form.cleaned_data['month'])
            month_half = int(lesson_reports_form.cleaned_data['month_half'])

            lessons = Lesson.objects.filter(
                teacher_id=request.user.id,
                is_passed=True,
                datetime__year=year,
                datetime__month=month,
                datetime__day__gt=0 if month_half == 1 else 15,
                datetime__day__lt=16 if month_half == 1 else 32
            ).order_by('datetime')

            for lesson in lessons:
                total += lesson.teacher_amount()
    else:
        lesson_reports_form = LessonReportsForm()

    return render(
        request,
        'lessons/reports.html',
        {
            'lessons': lessons,
            'form': lesson_reports_form,
            'year': year,
            'month': month,
            'total': total,
        }
    )


def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            comment = form.cleaned_data['client_comment']

            new_client = Client.objects.create(
                creator=request.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                comment=comment
            )

            return redirect('crm-create-subscription')
    else:
        form = ClientForm()

    return render(
        request,
        'lessons/create-client.html',
        {
            'form': form,
        }
    )


def create_client_subscription(request):
    if request.method == 'POST':
        form = ClientSubscriptionForm(request.POST)

        if form.is_valid():
            subscription = form.cleaned_data['subscription']
            client = form.cleaned_data['client']
            teacher = form.cleaned_data['teacher']
            comment = form.cleaned_data['comment']

            new_client_subscription = ClientSubscription.objects.create(
                creator=request.user,
                subscription=subscription,
                client=client,
                teacher=teacher,
                comment=comment,
            )

            return redirect('crm-subscription-lessons', client_subscription_id=new_client_subscription.pk)
    else:
        form = ClientSubscriptionForm()

    return render(
        request,
        'lessons/create-subscription.html',
        {
            'form': form,
        }
    )


def archive_client_subscription(request, client_subscription_id):
    client_subscription = get_object_or_404(ClientSubscription, pk=client_subscription_id)

    if request.user.groups.filter(name='Administrator').exists() and client_subscription.can_archive():
        client_subscription.status = Status.INACTIVE
        client_subscription.save()

    return redirect('crm-subscriptions')
