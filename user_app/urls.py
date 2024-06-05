
from django.contrib import admin
from django.urls import path
from . import views
from .controllers import user_view

urlpatterns = [
    path('', user_view.index_page ,name='index_page'),

    # genres 
    path('genres/<slug:genre_slug>/', user_view.genres_page, name='genres_page'),
    path('user-genres-list/<slug:slug>/', user_view.user_genres_list, name='user_genres_list'),
    
    # categories
      path('categories/<slug:category_slug>/', user_view.categories_page, name='categories_page'),
    path('user-categories-list/<slug:slug>/', user_view.user_categories_list, name='user_categories_list'),
    
  
    
    
    # Show
    
    # this is the endpoint that displays the modal popup for show details
      path('shows/<slug:show_slug>/', user_view.show_page, name='show_page'),
      
      # responsible for taking client the the actual video page
      path('show/watch/<slug:video_slug>/', user_view.video_page, name='video_page'),
    
    

     
]

