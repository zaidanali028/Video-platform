
from django.contrib import admin
from django.urls import path
from . import views
from .controllers import index_view

urlpatterns = [
    path('', index_view.index_page ,name='index_page'),
    path('video', index_view.video_page ,name='video_page'),
    path('video/detail', index_view.video_detail_page ,name='video_detail_page'),
    

     
]

