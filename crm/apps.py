from django.apps import AppConfig


class CrmConfig(AppConfig):
    name = 'crm'
    verbose_name = "Панель управления"


class AuthorizationConfig(AppConfig):
    name = 'AUTHENTICATION AND AUTHORIZATION'
    verbose_name = "Авторизация"
