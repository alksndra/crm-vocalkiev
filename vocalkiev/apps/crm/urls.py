from django.contrib import admin
from django.urls import path, include
from vocalkiev.apps.crm.apps.administrator.admin import administrator_admin_site
from vocalkiev.apps.crm.apps.teacher.admin import teacher_admin_site

from . import views

urlpatterns = [
    path('', views.index),
    path('schedule/', include('vocalkiev.apps.crm.apps.schedule.urls')),
    path('owner/', admin.site.urls),
    path('administrator/', administrator_admin_site.urls),
    path('teacher/', teacher_admin_site.urls),
]
