# dashboard/urls.py
from django.urls import path
from .views import prediction
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', prediction, name='prediction'),
    # Add more URL patterns as needed
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)