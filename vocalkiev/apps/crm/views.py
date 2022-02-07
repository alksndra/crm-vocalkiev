from django.shortcuts import redirect


def group_exists(request, group_name):
    if request.user.is_authenticated:
        if request.user.groups.filter(name=group_name).exists():
            return True
    return False


def index(request):
    if group_exists(request, 'Teacher'):
        return redirect('crm-lessons')

    if group_exists(request, 'Administrator'):
        return redirect('crm-lessons')

    return redirect('crm-schedule')
