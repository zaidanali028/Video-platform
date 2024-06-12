# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from ..models import User, Video,Show
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from admin_app.Forms.videos.Forms import VideoForm
from admin_app.services import FCS
import cloudinary.uploader
from custom_decorators.admin.decorators import staff_required,ensure_platform_configured
from admin_app.services import AppConfig



@staff_required
@ensure_platform_configured 
def videos_list(request):
    request.session['page'] = 'Admin Videos'
    staff_count = User.objects.filter(is_staff=True, is_active=True).count()
   
 
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    videos = Video.objects.all()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(videos, 5)  # Show 5 videos per page
    page_obj = paginator.get_page(page_number)

    context = {
        "videos": page_obj,
        "site_name":site_name,
        "site_logo":site_logo
    }
    return render(request, 'admin_app/partials/list_elements/videos_list.html', context)


@staff_required
@ensure_platform_configured 
def videos(request):
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    request.session['page'] = 'Admin Videos'
    staff_count = User.objects.filter(is_staff=True, is_active=True).count()

    context={
        "site_name":site_name,
        "site_logo":site_logo
    }
   
    return render(request, 'admin_app/pages/videos/videos.html',context)

@staff_required
@ensure_platform_configured 
def add_video(request):
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    shows=Show.objects.filter(status="true")
    if request.method == 'POST':
        
        # Make POST data mutable to manipulate it
        changed_data = request.POST.copy()
        
        # Retrieve files from the request
        video_file = request.FILES.get('video_url')
        thumb_image_url = request.FILES.get('thumb_image_url')
        
        # Validate and upload the thumbnail image
        if thumb_image_url:
            if thumb_image_url.content_type.startswith('image'):
                
                thumb_result = cloudinary.uploader.upload(thumb_image_url)
                changed_data['thumb_image_url'] = thumb_result['secure_url']
            else:
                changed_data['thumb_image_url'] = None  #invalid thumb_image_url file provided

        else:
            changed_data['thumb_image_url'] = None  # a thumb_image_url was not provided
        

        # Validate and upload the video file
        if video_file:
            if video_file.content_type.startswith('video'):
                # video_result = cloudinary.uploader.upload_large(video_file,)
                uploader=FCS.Uploader()
                changed_data['video_url'] =  uploader.upload(video_file)
                # print("changed_data['video_url']")
                # print(changed_data['video_url'])
                
            else:
                changed_data['video_url'] = None  #an invalid video_file was provded
        else:
            # a video file wasnt even specified
             changed_data['video_url'] = None  

        # Initialize the form with the updated data
        
        form = VideoForm(data=changed_data)

        if form.is_valid():
            # Save the form data to the database
            video=form.save(commit=False)
            video.user = request.user
            video.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'video_list_update'})

        else:
    
            # Add errors for invalid file types
            if thumb_image_url and not thumb_image_url.content_type.startswith('image'):
                # thumb_image_url provided but  its not of an image_file type
                form.add_error('thumb_image_url', 'Uploaded file is not an image.')
                
            if video_file and not video_file.content_type.startswith('video'):
                # video_file provided but  its not of an video_file type
                form.add_error('video_url', 'Uploaded file is not a video.')
            
          


                    

            # Render the form with errors
            return render(request, 'admin_app/partials/form_elements/videos/video_form.html', {
                'form': form,
                'shows':shows,
                "site_name":site_name,
                "site_logo":site_logo
                })

    else:
        # Initialize an empty form for GET requests
        form = VideoForm()

    return render(request, 'admin_app/partials/form_elements/videos/video_form.html', {
        'form': form,
        'shows':shows,
        "site_name":site_name,
        "site_logo":site_logo
    })

@staff_required
@ensure_platform_configured 
def edit_video(request, video_id):
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    video = get_object_or_404(Video, id=video_id)
    shows=Show.objects.filter(status="true")

    
    if request.method == 'POST':
        # Make POST data mutable to manipulate it
        changed_data = request.POST.copy()
        
        # Retrieve files from the request
        video_file = request.FILES.get('video_url')
        thumb_image_url = request.FILES.get('thumb_image_url')
        
        # Validate and upload the thumbnail image
        if thumb_image_url:
            if thumb_image_url.content_type.startswith('image'):
                thumb_result = cloudinary.uploader.upload(thumb_image_url)
                changed_data['thumb_image_url'] = thumb_result['secure_url']
            else:
                changed_data['thumb_image_url'] = video.thumb_image_url if video.thumb_image_url else None   # use defaulted one instead of None if the file specificed aint an image
        else:
            changed_data['thumb_image_url'] = video.thumb_image_url if video.thumb_image_url else None  #user is choosing to use the previously uploaded image
            

        # Validate and upload the video file
        if video_file:
            if video_file.content_type.startswith('video'):
                uploader=FCS.Uploader()
                changed_data['video_url'] =  uploader.upload(video_file)
                # video_result = cloudinary.uploader.upload_large(video_file)
                # changed_data['video_url'] = video_result['secure_url']
            
            else:
                changed_data['video_url'] = video.video_url if video.video_url else None  # use defaulted one instead of None if the file specificed aint an video
        else:
            changed_data['video_url'] = video.video_url if video.video_url else None   #user is choosing to use the previously uploaded video
            
            
    
        # Initialize the form with the updated data
        form = VideoForm(data=changed_data, instance=video)

        if form.is_valid():
            # Save the form data to the database
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'video_list_update'})
        else:
            # Add errors for invalid file types
            if thumb_image_url and not thumb_image_url.content_type.startswith('image'):
                form.add_error('thumb_image_url', 'Uploaded file is not an image.')
            if video_file:
                if not video_file.content_type.startswith('video'):
                    form.add_error('video_url', 'Uploaded file is not a video.')
                

            # Render the form with errors
            return render(request, 'admin_app/partials/form_elements/videos/video_form.html', {
                'form': form,
                'shows':shows,
                "site_name":site_name,
                "site_logo":site_logo
            })

    else:
        form = VideoForm(instance=video)
    
    return render(request, 'admin_app/partials/form_elements/videos/video_form.html', {
         'form': form,
         'shows':shows,
         "site_name":site_name,
         "site_logo":site_logo
    })


@staff_required
@ensure_platform_configured 
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.delete()
    return JsonResponse({'message': 'Video deleted successfully'})
