
from admin_app.models import Category,Genre,Video,Show,User
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from time import sleep
from django.db.models import Count
from admin_app.Forms.config_platform.Forms import UserForm
from admin_app.services import AppConfig
from django.utils.http import urlsafe_base64_decode

from custom_decorators.user.decorators  import ensure_auth



def index_page(request):
   request.session['page'] = 'Index'
   # get all users who has a brand_name
  
   user_with_brand = AppConfig.Ownership.get_owner()
   site_name = user_with_brand.brand_name if user_with_brand else None
   site_logo = user_with_brand.brand_image_url if user_with_brand else None

     
   # Retrieve just 5 newly created genres that have at least a show
   genres = Genre.objects.filter(status='active').annotate(genre_count=Count('genres_set')).filter(genre_count__gt=0).order_by('-created_at')[:5]
   #annotate(genre_count=Count('genres_set')): Adds a genre_count attribute to each genre, representing the number of related shows.
   # filter(genre_count__gt=0): Filters the genres to include only those where genre_count is greater than 0.
   # order_by('-created_at')[:5]: Orders the categories by created_at in descending order and limits the result to the first 5 categories.
   
   # Retrieve the latest 5 active categories that have at least a show
   categories = Category.objects.filter(status='active').annotate(show_count=Count('categories_set')).filter(show_count__gt=0).order_by('-created_at')[:5]
  #annotate(show_count=Count('categories_set')): Adds a show_count attribute to each category, representing the number of related shows.
  # filter(show_count__gt=0): Filters the categories to include only those where show_count is greater than 0.
  # order_by('-created_at')[:5]: Orders the categories by created_at in descending order and limits the result to the first 5 categories.


   
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
   

   

   
   context={'genre_with_shows':genre_with_shows,'site_name':site_name,'site_logo':site_logo,'random_picks':random_picks,'categories':categories,'genres':genres}
   
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
   

   
      

def user_genres_list(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    shows = Show.objects.filter(genres=genre, status='active')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(shows, 10)  # Show 10 genres per page
    page_obj = paginator.get_page(page_number)
    context = {"shows": page_obj, 'slug': slug}
    return render(request, 'user_app/partials/list_items/genres_list.html', context)

def genres_page(request, genre_slug):

    
   genre = get_object_or_404(Genre, slug=genre_slug)
   shows = Show.objects.filter(genres=genre, status='active')
   show_count = shows.count()
   page_title = ' '.join(genre_slug.split('-')).capitalize()
   request.session['page'] = page_title
   categories = Category.objects.filter(status='active').annotate(show_count=Count('categories_set')).filter(show_count__gt=0).order_by('-created_at')[:5]
   genres = Genre.objects.filter(status='active').annotate(genre_count=Count('genres_set')).filter(genre_count__gt=0).order_by('-created_at')[:5]
   random_picks = Show.objects.filter(status='active').order_by('?')[:5]
   user_with_brand = AppConfig.Ownership.get_owner()
  
   site_name = user_with_brand.brand_name if user_with_brand else None
   site_logo = user_with_brand.brand_image_url if user_with_brand else None
   context = {
        'genre_slug': genre_slug,
        'site_name': site_name,
        'site_logo':site_logo,
        'categories': categories,
        'genres':genres,
        'random_picks': random_picks,
        'page_title': page_title,
        'show_count': show_count,
   }
   return render(request, 'user_app/pages/genres/genres.html', context)

def user_categories_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    shows = Show.objects.filter(categories=category, status='active')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(shows, 10)  # Show 10 categories per page
    page_obj = paginator.get_page(page_number)
    context = {"shows": page_obj, 'slug': slug}
    return render(request, 'user_app/partials/list_items/categories_list.html', context)

def categories_page(request, category_slug):
   categories = Category.objects.filter(status='active').annotate(show_count=Count('categories_set')).filter(show_count__gt=0).order_by('-created_at')[:5]
   genres = Genre.objects.filter(status='active').annotate(genre_count=Count('genres_set')).filter(genre_count__gt=0).order_by('-created_at')[:5]
   category = get_object_or_404(Category, slug=category_slug)
   shows = Show.objects.filter(categories=category, status='active')
   show_count = shows.count()
   page_title = ' '.join(category_slug.split('-')).capitalize()
   request.session['page'] = page_title
   random_picks = Show.objects.filter(status='active').order_by('?')[:5]
   user_with_brand = AppConfig.Ownership.get_owner()

   site_name = user_with_brand.brand_name if user_with_brand else None
   site_logo = user_with_brand.brand_image_url if user_with_brand else None
   
   context = {
        'category_slug': category_slug,
        'site_name': site_name,
        'site_logo':site_logo,
        'categories': categories,
        'genres':genres,
        'random_picks': random_picks,
        'page_title': page_title,
        'show_count': show_count,
   }
   return render(request, 'user_app/pages/categories/categories.html', context)
 

    
    


def show_page(request,show_slug):
   show = get_object_or_404(Show, slug=show_slug)
   context={'show':show}
   
   
   return render(request, 'user_app/pages/shows/show.html', context)
  


@ensure_auth
def video_page(request,show_slug,video_slug):

   user_with_brand = AppConfig.Ownership.get_owner()

   genres = Genre.objects.filter(status='active').annotate(genre_count=Count('genres_set')).filter(genre_count__gt=0).order_by('-created_at')[:5]
   categories = Category.objects.filter(status='active').annotate(show_count=Count('categories_set')).filter(show_count__gt=0).order_by('-created_at')[:5]
   
   site_name=user_with_brand.brand_name if user_with_brand else None
   site_logo = user_with_brand.brand_image_url if user_with_brand else None
   
  
   # Get the show object based on the show_slug
   show = get_object_or_404(Show, slug=show_slug,status='active')
   page_title =" ".join(show.slug.split('-')).capitalize()
   request.session['page'] = page_title
   
    # Get the video object related to the show and video_slug
   video = get_object_or_404(Video, show=show, slug=video_slug,status='active')
   videos = show.video_set.filter(status="active")
   
   # these fields help in condtionallyy showing next and prev buttons on the video page
   current_index = list(videos).index(video)
   total_videos=videos.count()
   last_video_index = total_videos - 1

 

   # handling video and show view updates
   ip_address = request.META['REMOTE_ADDR']
   if request.session.get(f'viewed_{ip_address}'):
     
     
        # User has already viewed this video from this IP, don't increment view count
      pass
   else:
      # else increment both show and video view counts and set the session of that particular ip
      video.view_count += 1
      video.save()
      show.view_count += 1
      show.save()
      request.session[f'viewed_{ip_address}'] = True


  

    # Prepare the context with the show and video objects
   context = {
      'show': show,
      'video': video,
      'current_index':current_index,
      'last_video_index':last_video_index,
      'total_videos':total_videos ,
      'page_title':page_title,
      'site_name':site_name,
      'site_logo':site_logo,
      'categories':categories,
      'genres':genres

   }
   
   
   return render(request,'user_app/pages/video-detail.html',context)