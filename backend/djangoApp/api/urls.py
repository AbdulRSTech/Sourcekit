from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
        path('api/csrf/', views.get_csrf_token, name='get_csrf_token'), 
    path('api/saveKeyword/<str:word>', views.saveKeyword, name="saveKeyword"),
    path('api/save', views.save, name="save"),
    path('api/saveAndDownload', views.saveAndDownload, name="saveAndDownload"),
    path('api/download/<int:id>/<str:format>', views.download, name="download"),
    path('api/delete/<int:id>', views.delete, name="delete")
]