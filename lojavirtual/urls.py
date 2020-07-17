from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('openapi/', get_schema_view(
        title="Your Project",
        description="API for all things …"
    ), name='openapi-schema'),
    path('', include('core.urls'))
]
