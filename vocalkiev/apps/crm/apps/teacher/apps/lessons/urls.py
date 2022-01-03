from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='crm-teacher-lessons'),
    path('reports', views.reports, name='crm-teacher-reports'),
    path('subscriptions/', views.show_subscriptions, name='crm-teacher-subscriptions'),
    path(
        'subscriptions/<int:client_subscription_id>/lessons/',
        views.show_lessons,
        name='crm-teacher-subscription-lessons'
    ),
    path(
        'subscriptions/<int:client_subscription_id>/lessons/create/',
        views.create_lesson,
        name='crm-teacher-create-lesson'
    ),
    path('<int:lesson_id>/pass/', views.pass_lesson, name='crm-teacher-pass-lesson'),
    path('<int:lesson_id>/update/', views.update_lesson, name='crm-teacher-update-lesson'),
]
