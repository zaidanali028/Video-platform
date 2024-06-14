from django.shortcuts import render,redirect
from admin_app.models  import User

from django.http import HttpResponse
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from admin_app.Forms.config_platform.Forms import EmailValidationForm,NameValidationForm,BrandNameValidationForm,PhoneNumberValidationForm,PasswordChangeForm,UserForm,ConfigUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from admin_app.services import AppConfig
from custom_decorators.admin.decorators import staff_required,ensure_platform_configured
from admin_app.services import AppConfig
from django.views.decorators.http import require_POST
from django.contrib.auth import login
import cloudinary.uploader
from time import sleep

from django.urls import reverse
def config_platform(request):
    request.session['page'] = 'Configure Your Platform'
    staff_count = User.objects.filter(is_staff=True, is_active=True).count()
    if staff_count < 2:
        context = {
            'class': '',  # Proviinge a default value for class
            'msg': '',  # Providing a default value for msg
            # Other context variables
        }
        return render(request, 'admin_app/pages/config/config_platform.html', context)
    else:
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            # Handle the case when there's no referer URL
            return redirect(reverse('admin_index') )  # back to admin_index page

    





@require_POST
def post_config(request):
    
     # Make POST data mutable to manipulate it
    changed_data = request.POST.copy()
    brand_image_url = request.FILES.get('brand_image_url')
    brand_image=''
    
     # Validate and upload the brand_image
    if brand_image_url:
            if brand_image_url.content_type.startswith('image'):
                # pass if the content_type aint an image
                
                brand_image_result = cloudinary.uploader.upload(brand_image_url)
                changed_data['brand_image_url'] = brand_image_result['secure_url']
                brand_image=  changed_data['brand_image_url'] 
                
            else:
                changed_data['brand_image_url'] =None
    else:
            changed_data['brand_image_url'] = None 
    form = UserForm(data=changed_data)
    context = {field: request.POST.get(field) for field in ['email', 'name', 'phone_number', 'brand_name', 'password']}
    # print(context)
    
    if form.is_valid():
        # Form data is valid, save the user
        
        user=form.save(commit=False)
        user.name=user.name.lower()
        user.username=user.name 
        user.is_staff=True
        user.brand_name=user.brand_name.lower()
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request,user)
        # print('rev:' +reverse('admin_index') + '?success=true')
        # Return JSON response with redirect URL
        # Return JSON response with redirect header
        response = JsonResponse({'success': True})
        to_admin_panel=reverse('admin_index') + '?success=true'
        response['HX-Redirect'] =to_admin_panel
        return response 
    else:
        if brand_image_url and not brand_image_url.content_type.startswith('image'):
                form.add_error('brand_image_url', 'Uploaded file is not an image.')
        # Form data is invalid, collect errors
        errors = {f'err_{field}': error_list[0] for field, error_list in form.errors.items()}
          # 'err_'field because eachfied is accessible by the field name to display its value
            # am adding err to the field ,example err_email so that it doesnt conflict with the email's value
               # Include brand_name in the context
               

        # Merge errors into context
        context.update(errors)
        context.update({'brand_image':brand_image})


    html_content = render_to_string('admin_app/partials/form_elements/config_platform_res.html', context=context)
    return HttpResponse(html_content)

   

@require_POST
def validate_email(request):
    validation_response = {
        "msg": "",
        "class": "",
        "email": request.POST.get('email', '')
    }

    form = EmailValidationForm(request.POST)
    if form.is_valid():
        if form.unique_email():
            validation_response['msg'] = 'This email is valid'
            validation_response['class'] = 'text-green-700'
        else:
            validation_response['msg'] = 'This email already exists'
            validation_response['class'] = 'text-red-700'
    else:
        validation_response['msg'] = form.errors.get('email', 'Email is required')
        validation_response['class'] = 'text-red-700'

    html_content = render_to_string('admin_app/partials/form_elements/email_res.html', context=validation_response)
    return HttpResponse(html_content)



@require_POST
def validate_name(request):
    validation_response = {
        "msg": "",
        "class": "",
        "name": request.POST.get('name', '')
    }

    form = NameValidationForm(request.POST)
    if form.is_valid():
        if form.unique_name():
            validation_response['msg'] = 'This name is valid'
            validation_response['class'] = 'text-green-700'
        else:
            validation_response['msg'] = 'This name already exists'
            validation_response['class'] = 'text-red-700'
    else:
        validation_response['msg'] = form.errors.get('name', 'Name is required')
        validation_response['class'] = 'text-red-700'

    html_content = render_to_string('admin_app/partials/form_elements/name_res.html', context=validation_response)
    return HttpResponse(html_content)

@require_POST
def validate_phone_number(request):
    validation_response = {
        "msg": "",
        "class": "",
        "phone_number": request.POST.get('phone_number', '')
    }

    form = PhoneNumberValidationForm(request.POST)
    if form.is_valid():
        if form.unique_phone_number():
            validation_response['msg'] = 'This phone number is valid'
            validation_response['class'] = 'text-green-700'
        else:
            validation_response['msg'] = 'This phone number already exists'
            validation_response['class'] = 'text-red-700'
    else:
        validation_response['msg'] = form.errors.get('phone_number', 'Phone number is required')
        validation_response['class'] = 'text-red-700'

    html_content = render_to_string('admin_app/partials/form_elements/phone_number_res.html', context=validation_response)
    return HttpResponse(html_content)

@require_POST
def validate_brand_name(request):
    validation_response = {
        "msg": "",
        "class": "",
        "brand_name": request.POST.get('brand_name', '')
    }

    form = BrandNameValidationForm(request.POST)
    if form.is_valid():
        if form.unique_brand_name():
            validation_response['msg'] = 'This brand name is valid'
            validation_response['class'] = 'text-green-700'
        else:
            validation_response['msg'] = 'This brand name already exists'
            validation_response['class'] = 'text-red-700'
    else:
        validation_response['msg'] = form.errors.get('brand_name', 'Brand name is required')
        validation_response['class'] = 'text-red-700'

    html_content = render_to_string('admin_app/partials/form_elements/brand_name_res.html', context=validation_response)
    return HttpResponse(html_content)


    

@require_POST
def validate_password(request):
    password=request.POST.get('password')
    confirm_password=request.POST.get('confirm_password')

    validation_response = {
        "msg": "",
        "class": "",
        "password":password,
        "confirm_password":confirm_password
    }
    # print(validation_response)

    form = PasswordChangeForm(request.POST)
    if form.is_valid():
        # Passwords match
        if form.password_match(password,confirm_password):
            validation_response['msg'] = 'Password is valid'
            validation_response['class'] = 'text-green-700'
        else:
            validation_response['msg'] = 'Passwords do not match'
            validation_response['class'] = 'text-red-700'
    else:
        # Passwords don't match or validation failed

        validation_response['msg'] = form.errors.get('password')
        validation_response['class'] = 'text-red-700'

    html_content = render_to_string('admin_app/partials/form_elements/password_res.html', context=validation_response)
    return HttpResponse(html_content)

@staff_required
@ensure_platform_configured 
def admin_config(request):
    # modifies user model from the admin panel
    
    request.session['page'] = 'Admin Config'
    user = request.user
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    
    
    
    if request.method == 'POST':
        
        # Make POST data mutable to manipulate it
        changed_data = request.POST.copy()
        
        # Retrieve the cover image file from the request
        brand_image_url = request.FILES.get('brand_image_url')
        
 
        # Validate and upload the cover image
        if brand_image_url:
            if brand_image_url.content_type.startswith('image'):
                brand_image_ressult = cloudinary.uploader.upload(brand_image_url)
                changed_data['brand_image_url'] = brand_image_ressult['secure_url']
            else:
                changed_data['brand_image_url'] = user.brand_image_url if user.brand_image_url else None  # use previous one if the uploaded file isn't an image
        else:
            changed_data['brand_image_url'] = user.brand_image_url if user.brand_image_url else None  # use the previously uploaded image if no new image is provided
        
        form = ConfigUpdateForm(data=changed_data)
        
      
            
                
           
        
                

        # Initialize the form with the updated data
        if form.is_valid():
            user.name=form.cleaned_data.get('name')
            user.email=form.cleaned_data.get('email')
            user.brand_name=form.cleaned_data.get('brand_name')
            user.phone_number=form.cleaned_data.get('phone_number')
            user.brand_image_url=form.cleaned_data.get('brand_image_url')
            user.save()
 


            response = JsonResponse({'success': True})
            to_admin_panel=reverse('admin_index') + '?updated=true'
            response['HX-Redirect'] =to_admin_panel
            return response 
            
        else:
           
            
            return render(request, 'admin_app/partials/form_elements/config/config_form.html',{
                'form':form,
                # 'password':password,
                # 'confirm_password':confirm_password,
                 'site_name':site_name,
                 'site_logo':site_logo
                })
            
    else:
        # form with just user instance
        form = ConfigUpdateForm(initial={
            "name":user.name,
            "email":user.email,
            "brand_name":user.brand_name,
            "phone_number":user.phone_number,
            "brand_image_url":user.brand_image_url,
        })
        
    
    
    return render(request, 'admin_app/pages/config/admin_config.html',{
        'form':form,
        'site_name':site_name,
        'site_logo':site_logo
        })
    