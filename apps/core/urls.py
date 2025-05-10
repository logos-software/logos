"""
URLs para o aplicativo core.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('health/', views.health_check, name='health_check'),
]
