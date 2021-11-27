from django.shortcuts import redirect


def index(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Teacher').exists():
            return redirect('crm-teacher-lessons')

    return redirect('crm-schedule')
