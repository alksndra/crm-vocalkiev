from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('schedule/', include('vocalkiev.apps.crm.apps.schedule.urls')),
    path('owner/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('teacher/', admin.site.urls),
]
