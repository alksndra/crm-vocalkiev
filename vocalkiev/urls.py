from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from vocalkiev.settings import LOGIN_URL
from vocalkiev.apps.owner.admin import owner_admin_site
from django.contrib.auth.decorators import login_required, user_passes_test
from decorator_include import decorator_include
from django.contrib.auth.views import LoginView

urlpatterns = [
    path(LOGIN_URL, LoginView.as_view(template_name='admin/login.html'))
]

urlpatterns += i18n_patterns(
    path('', include('vocalkiev.apps.vocalkiev_com.urls')),
    path('report_builder/', include('report_builder.urls')),
    path('owner/',
         decorator_include(user_passes_test(lambda u: u.is_superuser, login_url=f'/{LOGIN_URL}'),
                           owner_admin_site.urls)
         ),
    path('crm/', decorator_include(login_required(login_url=f'/{LOGIN_URL}'), include('vocalkiev.apps.crm.urls'))),
)
