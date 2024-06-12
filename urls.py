from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('webcam/', views.webcam_view, name='webcam'),
    path('phone/', views.phone_view, name='phone'),
]
