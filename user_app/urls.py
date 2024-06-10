
from django.contrib import admin
from django.urls import path
from .controllers import user_view,auth_view

urlpatterns = [
    path('', user_view.index_page ,name='index_page'),
    
    
    # auth endpoints
    path('auth/register/', auth_view.registration_page ,name='registration_page'),
     # user account activation from email
    path('auth/activate/<uidb64>/<token>/', auth_view.activate_user, name='activate_user'),
    # forgot-password
    path('auth/forgot-password/', auth_view.forgot_password_page ,name='forgot_password_page'),
     # login
    path('auth/login/', auth_view.login_page ,name='login_page'),
    # logout
    path('auth/logout/', auth_view.logout_page ,name='logout_page'),
   
    
       # user account reset from email
    path('auth/reset/<uidb64>/<token>/', auth_view.password_reset_confirm, name='password_reset_confirm'),
    

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
    path('show/<slug:show_slug>/watch/<slug:video_slug>/', user_view.video_page, name='video_page'),

    

     
]

