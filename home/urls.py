from . import views
from django.urls import path

urlpatterns = [
    path('', views.Main.as_view(), name='home'),
    path('#<path:url>', views.Api.as_view(), name='api'),
]