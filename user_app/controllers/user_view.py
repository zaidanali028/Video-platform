
from django.http import HttpResponse
from admin_app.models import Category,Genre,Video,Show,User
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from time import sleep

def index_page(request):
   request.session['page'] = 'Index'
   # get all users who has a brand_name
   # 1. (brand_name__isnull=True), will return users with no brand name
   # 2 ...exclude() will filter out and return only users with brand name
   # 3. .first() will get the first user that matches the above criteria
   
   user_with_brand = User.objects.filter(brand_name__isnull=False).first()
   if user_with_brand:
 
      site_name=user_with_brand.brand_name

     
   # Retrieve all genres
   genres = Genre.objects.filter(status='active')
   
   # Retrieve the latest 5 active categories
   categories = Category.objects.filter(status='active').order_by('-created_at')[:5]
   
   # get random shows from db
   random_picks= Show.objects.filter(status='active').order_by('?')[:5]

    # Initialize a dictionary to store shows by genre
   genre_with_shows = {}

    # Loop through each genre and retrieve a limited number of shows associated with it
   for genre in genres:
      
        # Retrieve a limited number of active shos associated with the genre 
        shows = Show.objects.filter(genres=genre,status='active')[:6]
        
        
        
       # Only add to the dictionary if there are any videos
        if shows.exists():
          # Add the videos to the dictionary with the genre name as key
         genre_with_shows[genre.name] = {"shows":shows}
   

   

   
   context={'genre_with_shows':genre_with_shows,'site_name':site_name,'random_picks':random_picks,'categories':categories}
   
   # response example('genre_with_shows'):
#  ==============  
# {'New Releases': {'shows': <QuerySet [<Show: Fate stay night>]>}, 
# 'Sports': {'shows': <QuerySet [<Show: Rhinestones>]>}, 
# 'War': {'shows': <QuerySet [<Show: Rhinestones>]>}, 
# 'Mystery': {'shows': <QuerySet [<Show: Fate stay night>]>}, 
# 'Fantasy': {'shows': <QuerySet [<Show: Fate stay night>]>},
# 'Live Action': {'shows': <QuerySet [<Show: Rhinestones>]>}}
#  ================

   # print(genre_with_shows)
 
   
   
   return render(request,'user_app/pages/user_index.html',context)
   
def user_genres_list(request,slug):
   genre = get_object_or_404(Genre, slug=slug)
   
   shows = Show.objects.filter(genres=genre,status='active')
   page_number = request.GET.get('page', 1)
   paginator = Paginator(shows, 10)  # Show 10 genres per page
   page_obj = paginator.get_page(page_number)
   context= { "shows":page_obj,'slug':slug}

   return render(request,'user_app/partials/list_items/genres_list.html',context)
   


def genres_page(request,genre_slug):
   # get all categories
   categories = Category.objects.filter(status='active')
   # find genre by provided slug
   genre = get_object_or_404(Genre, slug=genre_slug)
   
   # count its shows
   shows = Show.objects.filter(genres=genre,status='active')
   show_count=shows.count()
   
   
   
   page_title = ' '.join(genre_slug.split('-')).capitalize()
   request.session['page'] = page_title
    # Retrieve the latest 5 active categories
   categories = Category.objects.filter(status='active').order_by('-created_at')[:5]
   # get all users who has a brand_name
   # 1. (brand_name__isnull=True), will return users with no brand name
   # 2 ...exclude() will filter out and return only users with brand name
   # 3. .first() will get the first user that matches the above criteria
   
   # get random shows from db
   random_picks= Show.objects.filter(status='active').order_by('?')[:5]
   
   user_with_brand = User.objects.filter(brand_name__isnull=False).first()
   if user_with_brand:
 
      site_name=user_with_brand.brand_name
   
  

      
   # Retrieve a limited number of active shos associated with the genre 
        
        
        
    
   context={'genre_slug':genre_slug,'site_name':site_name,'categories':categories,'random_picks':random_picks,'page_title':page_title,'show_count':show_count}
   return render(request,'user_app/pages/genres/genres.html',context)
def video_page(request):
   
   return HttpResponse('Video Page :)')


def video_detail_page(request):
   
   return HttpResponse('Video Detail Page :)')
