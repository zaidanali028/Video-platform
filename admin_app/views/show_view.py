from django.shortcuts import render, get_object_or_404
from ..models import User, Show
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from admin_app.Forms.shows.Forms import ShowForm
import cloudinary.uploader
from custom_decorators.admin.decorators import staff_required,ensure_platform_configured
from admin_app.services import AppConfig


@staff_required
@ensure_platform_configured   
def shows_list(request):
    request.session['page'] = 'Admin Shows'
    staff_count = User.objects.filter(is_staff=True, is_active=True).count()
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    shows = Show.objects.all()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(shows, 10)  # Show 10 shows per page
    page_obj = paginator.get_page(page_number)

    context = {
        "shows": page_obj,
        "site_name":site_name,
        "site_logo":site_logo
    }
    
    return render(request, 'admin_app/partials/list_elements/shows_list.html', context)

@staff_required
@ensure_platform_configured   
def shows(request):
    request.session['page'] = 'Admin Shows'
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    staff_count = User.objects.filter(is_staff=True, is_active=True).count()
    context={
        "site_name":site_name,
        "site_logo":site_logo
    }
   
    return render(request, 'admin_app/pages/shows/shows.html',context)

@staff_required
@ensure_platform_configured   
def add_show(request):
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    if request.method == 'POST':
        # Make POST data mutable to manipulate it
        changed_data = request.POST.copy()
        
        # Retrieve the cover image file from the request
        cover_image_url = request.FILES.get('cover_image_url')
        
        # Validate and upload the cover image
        if cover_image_url:
            if cover_image_url.content_type.startswith('image'):
                cover_result = cloudinary.uploader.upload(cover_image_url)
                changed_data['cover_image_url'] = cover_result['secure_url']
            else:
                changed_data['cover_image_url'] = None  # To avoid failing validation later
        
        # this is to prevent making a show active when it does not have any video attached to it
        changed_data['status']='inactive'
        
        # Initialize the form with the updated data
        form = ShowForm(data=changed_data)

        if form.is_valid():
            show=form.save()
            # this is to prevent making a show active when it does not have any video attached to it
          
            return HttpResponse(status=204, headers={'HX-Trigger': 'show_list_update'})
        else:
            # Add errors for invalid file types
            if cover_image_url and not cover_image_url.content_type.startswith('image'):
                form.add_error('cover_image_url', 'Uploaded file is not an image.')

            # Render the form with errors
            return render(request, 'admin_app/partials/form_elements/shows/show_form.html', {
                'form': form,
                "site_name":site_name,
                "site_logo":site_logo
                })

    else:
        # Initialize an empty form for GET requests
        form = ShowForm()

    return render(request, 'admin_app/partials/form_elements/shows/show_form.html', {'form': form})

@staff_required
@ensure_platform_configured   
def edit_show(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    if request.method == 'POST':
        
        # Make POST data mutable to manipulate it
        changed_data = request.POST.copy()
        
        # Retrieve the cover image file from the request
        cover_image_url = request.FILES.get('cover_image_url')
        
        # Validate and upload the cover image
        if cover_image_url:
            if cover_image_url.content_type.startswith('image'):
                cover_result = cloudinary.uploader.upload(cover_image_url)
                changed_data['cover_image_url'] = cover_result['secure_url']
            else:
                changed_data['cover_image_url'] = show.cover_image_url if show.cover_image_url else None  # use previous one if the uploaded file isn't an image
        else:
            changed_data['cover_image_url'] = show.cover_image_url if show.cover_image_url else None  # use the previously uploaded image if no new image is provided

        # Initialize the form with the updated data
        form = ShowForm(data=changed_data, instance=show)
        
            # Perform additional validation
        active_videos_count = show.video_set.filter(status='active').count()

        if active_videos_count < 1 and changed_data.get('status') == 'active':
            form.add_error('status', 'At least one[active] video is required to set status to active for this show') 

        if form.is_valid():
            # Save the form data to the database
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'show_list_update'})
        else:
            # Add errors for invalid file types
            if cover_image_url and not cover_image_url.content_type.startswith('image'):
                form.add_error('cover_image_url', 'Uploaded file is not an image.')

            # Render the form with errors
            return render(request, 'admin_app/partials/form_elements/shows/show_form.html', {
                'form': form,
                 "site_name":site_name,
                 "site_logo":site_logo
                })

    else:
        form = ShowForm(instance=show)
    
    return render(request, 'admin_app/partials/form_elements/shows/show_form.html', {
        'form': form,
        "site_name":site_name,
        "site_logo":site_logo
        })

@staff_required
@ensure_platform_configured   
def delete_show(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    show.delete()
    return JsonResponse({'message': 'Show deleted successfully'})
