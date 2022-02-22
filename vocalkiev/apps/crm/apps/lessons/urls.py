from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='crm-lessons'),
    path('reports', views.reports, name='crm-reports'),
    path('clients/create', views.create_client, name='crm-create-client'),
    path('subscriptions', views.show_subscriptions, name='crm-subscriptions'),
    path(
        'subscriptions/create/',
        views.create_client_subscription,
        name='crm-create-subscription'
    ),
    path(
        'subscriptions/create-rent/',
        views.create_rent_subscription,
        name='crm-create-rent'
    ),
    path(
        'subscriptions/<int:client_subscription_id>/archive/',
        views.archive_client_subscription,
        name='crm-archive-subscription'
    ),
    path(
        'subscriptions/<int:client_subscription_id>/lessons/',
        views.show_lessons,
        name='crm-subscription-lessons'
    ),
    path(
        'subscriptions/<int:client_subscription_id>/lessons/create/',
        views.create_lesson,
        name='crm-create-lesson'
    ),
    path('<int:lesson_id>/pass/', views.pass_lesson, name='crm-pass-lesson'),
    path('<int:lesson_id>/update/', views.update_lesson, name='crm-update-lesson'),
]
