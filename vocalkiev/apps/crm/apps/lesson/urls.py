from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='crm-lesson'),
    path('<int:client_subscription_id>/', views.lesson),
]
