from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='crm-lesson'),
    path('reports', views.reports, name='crm-lesson-reports'),
    path('subscriptions/', views.show_subscriptions, name='crm-subscriptions'),
    path('subscriptions/<int:client_subscription_id>/lessons/', views.show_lessons, name='crm-subscription-lessons'),
    path('subscriptions/<int:client_subscription_id>/lessons/create/', views.create_lesson, name='crm-create-lesson'),
    path('lessons/<int:lesson_id>/pass/', views.pass_lesson, name='crm-pass-lesson'),
]
