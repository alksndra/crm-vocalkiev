from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from vocalkiev.apps.owner.admin import owner_admin_site

urlpatterns = [
]

urlpatterns += i18n_patterns(
    path('', include('vocalkiev.apps.vocalkiev_com.urls')),
    path('owner/', owner_admin_site.urls),
    path('crm/', include('vocalkiev.apps.crm.urls')),
)
