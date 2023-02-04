from django.urls import path
from . import views


urlpatterns = [
    path('',views.upload_images,name='upload'),
    path('search/', views.search, name='search'),
    path('display/', views.display_images, name='display'),
]