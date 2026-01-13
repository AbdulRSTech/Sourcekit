from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/csrf/', views.get_csrf_token, name='get_csrf_token'), 
]