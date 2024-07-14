from django.contrib import admin
from django.urls import path, include
from short import views

from django.urls import path
from .views import home, success, upload_img, display_your_camera, process_frame

urlpatterns = [
    path('', home, name='home'),
    path('success/', success, name='success'),
    path('upload_img/', upload_img, name='upload_img'),
    path('display_your_camera/', display_your_camera, name='display_your_camera'),
    path('process_frame/', process_frame, name='process_frame'),
]
