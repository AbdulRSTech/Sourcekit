from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
        path('api/csrf/', views.get_csrf_token, name='get_csrf_token'), 
    path('api/saveKeyword/<str:word>', views.saveKeyword, name="saveKeyword"),
    path('api/save', views.save, name="save"),
    path('api/saveAndDownload', views.saveAndDownload, name="saveAndDownload"),
    path('api/download/<int:id>/<str:format>', views.download, name="download"),
    path('api/allResources', views.allResources, name="allResources"),
    path('api/searchTitle/<str:title>', views.searchTitle, name="searchTitle"),
    path('api/searchKeywords/<str:keywords', views.searchKeywords, name="searchKeywords"),
    path('api/search/<str:title>/<str:keywords>', views.search, name="search"),
    path('api/updateResource', views.updateResource, name="updateResource"),
    path('api/deleteResource', views.deleteResource, name="deleteResource"),
    path('api/deleteKeyword', views.deleteKeyword, name="deleteKeyword")
]