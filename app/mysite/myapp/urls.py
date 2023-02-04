from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('search/', views.search, name='search'),
    path('upload/', views.upload_folder, name='upload'),
    path('display/', views.display_images, name='display'),
]