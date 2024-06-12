
from django.contrib import admin
from django.urls import path
from . import views
from .controllers import config_view,auth_view,admin_view,genre_view,category_view,video_view,show_view

urlpatterns = [
    path('config-platform/', config_view.config_platform ,name='config_platform'),
    path('post-config/', config_view.post_config ,name='post-config'),
    path('post-config/validate-email', config_view.validate_email ,name='validate_email'),
    path('post-config/validate-name', config_view.validate_name, name='validate_name'),
    path('post-config/validate-phone-number', config_view.validate_phone_number, name='validate_phone_number'),
    path('post-config/validate-brand-name', config_view.validate_brand_name, name='validate_brand_name'),
    path('post-config/validate-password', config_view.validate_password, name='validate_password'),
    # path('post-config/validate-brand-image-url', config_view.validate_brand_image_url, name='validate_brand_image_url'),
    #    config for admin panel
    path('admin-config/', config_view.admin_config ,name='admin_config'),
    path('auth/update-password/', auth_view.admin_update_password ,name='admin_update_password'),
    

    # admin-endpoint
    path('', admin_view.admin_index ,name='admin_index'),
   

# Genres
  path('genres/', genre_view.genres, name='genres'),
  path('genres-list/', genre_view.genres_list, name='genres_list'),
  path('genres/add/', genre_view.add_genre, name='add_genre'),
  path('genres/edit/<int:genre_id>/', genre_view.edit_genre, name='edit_genre'),
  path('genres/delete/<int:genre_id>/', genre_view.delete_genre, name='delete_genre'),


    # Categories
    path('categories/', category_view.categories, name='categories'),
    path('categories-list/', category_view.categories_list, name='categories_list'),
    path('categories/add/', category_view.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', category_view.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', category_view.delete_category, name='delete_category'),
    
     # Shows
    path('shows/', show_view.shows, name='shows'),
    path('shows-list/', show_view.shows_list, name='shows_list'),
    path('shows/add/', show_view.add_show, name='add_show'),
    path('shows/edit/<int:show_id>/', show_view.edit_show, name='edit_show'),
    path('shows/delete/<int:show_id>/', show_view.delete_show, name='delete_show'),

 # Videos
    path('videos/', video_view.videos, name='videos'),
    path('videos-list/', video_view.videos_list, name='videos_list'),
    path('videos/add/', video_view.add_video, name='add_video'),
    path('videos/edit/<int:video_id>/', video_view.edit_video, name='edit_video'),
    path('videos/delete/<int:video_id>/', video_view.delete_video, name='delete_video'),



# auth endpoints
    path('login/', auth_view.admin_login ,name='admin_login'),

   
   


     
]

