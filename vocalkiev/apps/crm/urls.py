from decorator_include import decorator_include
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.urls import path, include
from vocalkiev.apps.crm.apps.administrator.admin import administrator_admin_site
from vocalkiev.apps.crm.apps.teacher.admin import teacher_admin_site
from vocalkiev.settings import LOGIN_URL
from . import views


def only_in_group(group_name):
    def check(user: User):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()

    return user_passes_test(check, login_url=f'/{LOGIN_URL}')


urlpatterns = [
    path('', views.index, name='crm-index'),
    path('schedule/', include('vocalkiev.apps.crm.apps.schedule.urls')),
    path('lessons/', include('vocalkiev.apps.crm.apps.lessons.urls')),
    path(
        'administrator/admin/',
        decorator_include(
            only_in_group('Administrator'),
            administrator_admin_site.urls,
        ),
    ),
    path(
        'teacher/admin/',
        decorator_include(
            only_in_group('Teacher'),
            teacher_admin_site.urls,
        ),
    ),
]
