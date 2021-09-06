from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('schedule/<int:year>/<int:month>/<int:day>/<int:place_id>/', views.schedule_day),
    path('schedule/<int:year>/<int:month>/<int:day>/', views.schedule_day),
    path('schedule/<int:year>/<int:month>/', views.schedule_day),
    path('schedule/<int:year>/', views.schedule_day),
    path('schedule/', views.schedule_day),
    path('schedule', views.schedule),
]
