from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from csvfile.views import category_upload

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('upload-csv/', category_upload, name='category_upload'),
    path('api/', include('authentication.urls')),
    path('api/', include('api.urls')),
]
