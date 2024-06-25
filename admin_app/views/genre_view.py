from django.shortcuts import render,get_object_or_404
from ..models import User
from django.http import HttpResponse,JsonResponse
from admin_app.models import Genre
from admin_app.Forms.genres.Forms import GenreForm
from django.core.paginator import Paginator
from custom_decorators.admin.decorators import staff_required,ensure_platform_configured
from admin_app.services import AppConfig




@staff_required
@ensure_platform_configured   
def genres_list(request):
   
   request.session['page'] = 'Admin Genres'
   user_with_brand = AppConfig.Ownership.get_owner()
   site_name = user_with_brand.brand_name if user_with_brand else None
   site_logo = user_with_brand.brand_image_url if user_with_brand else None
   staff_count = User.objects.filter(is_staff=True, is_active=True).count()
   page_number = request.GET.get('page', 1)
   genres = Genre.objects.all()
   paginator = Paginator(genres, 10)  # Show 10 genres per page
   page_obj = paginator.get_page(page_number)

 
   context={
     "genres":page_obj,
     "site_name":site_name,
     "site_logo":site_logo
   }
#    return HttpResponse(genres)
   return render(request,'admin_app/partials/list_elements/genres_list.html',context)


@staff_required
@ensure_platform_configured   
def genres(request):
   request.session['page'] = 'Admin Genres'
   user_with_brand = AppConfig.Ownership.get_owner()
   site_name = user_with_brand.brand_name if user_with_brand else None
   site_logo = user_with_brand.brand_image_url if user_with_brand else None
   staff_count = User.objects.filter(is_staff=True, is_active=True).count()
   context={
      "site_name":site_name,
      "site_logo":site_logo
   }
   return render(request,'admin_app/pages/genres/genres.html',context)


@staff_required
@ensure_platform_configured 
def add_genre(request):

    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    if request.method == 'POST':

        form = GenreForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse(status=204,headers={'HX-Trigger':'genre_list_update'}) #No content is returned
       


    else:
        # creation of a new form
        form = GenreForm()
        print(form)
        

    return render(request, 'admin_app/partials/form_elements/genres/genre_form.html', {
        'form':form,
        "site_name":site_name,
        "site_logo":site_logo})

@staff_required
@ensure_platform_configured 
def edit_genre(request, genre_id):
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    genre = get_object_or_404(Genre, id=genre_id)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204,headers={'HX-Trigger':'genre_list_update'}) #No content is returned

    else:
        form = GenreForm(instance=genre)
    return render(request, 'admin_app/partials/form_elements/genres/genre_form.html', {
        'form':form,
        "site_name":site_name,
        "site_logo":site_logo
        })


@staff_required
@ensure_platform_configured 
def delete_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    genre.delete()
    # return redirect('genres_list')
    return JsonResponse({'message': 'Genre deleted successfully'})