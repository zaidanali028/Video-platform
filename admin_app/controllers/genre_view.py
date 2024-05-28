from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from ..models import User
from django.http import HttpResponse,JsonResponse
from admin_app.models import Genre
from admin_app.Forms.genres.Forms import GenreForm
from django.core.paginator import Paginator
@login_required(login_url='admin_login')    
def genres_list(request):
   print('wow')
   request.session['page'] = 'Admin Genres'
   staff_count = User.objects.filter(is_staff=True, is_active=True).count()
   if staff_count<2:
        # super super admin and the admin using the platform,will take admin to config_platform incase the staff accounts aint 2
        return redirect('config_platform')
   genres = Genre.objects.all()
   page_number = request.GET.get('page', 1)
   genres = Genre.objects.all()
   paginator = Paginator(genres, 10)  # Show 10 genres per page
   page_obj = paginator.get_page(page_number)

 
   context={
     "genres":page_obj  
   }
#    return HttpResponse(genres)
   return render(request,'admin_app/partials/list_elements/genres_list.html',context)


@login_required(login_url='admin_login')    
def genres(request):
   request.session['page'] = 'Admin Genres'
   staff_count = User.objects.filter(is_staff=True, is_active=True).count()
   if staff_count<2:
        # super super admin and the admin using the platform,will take admin to config_platform incase the staff accounts aint 2
        return redirect('config_platform')
   context={
      
   }
   return render(request,'admin_app/pages/genres/genres.html',context)

def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse(status=204,headers={'HX-Trigger':'genre_list_update'}) #No content is returned
       


    else:
        # creation of a new form
        form = GenreForm()
        print(form)
        

    return render(request, 'admin_app/partials/form_elements/genres/genre_form.html', {'form':form})

def edit_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204,headers={'HX-Trigger':'genre_list_update'}) #No content is returned

    else:
        form = GenreForm(instance=genre)
    return render(request, 'admin_app/partials/form_elements/genres/genre_form.html', {'form':form})


def delete_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    genre.delete()
    # return redirect('genres_list')
    return JsonResponse({'message': 'Genre deleted successfully'})