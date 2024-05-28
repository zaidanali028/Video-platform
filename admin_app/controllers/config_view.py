from django.shortcuts import render,redirect
from ..models import User
from django.http import HttpResponse

import re
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from admin_app.Forms.config_platform.Forms import EmailValidationForm,NameValidationForm,BrandNameValidationForm,PhoneNumberValidationForm,PasswordChangeForm,UserForm
from django.views.decorators.http import require_POST
from django.contrib.auth import login
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

    


def admin_login(request):
    return HttpResponse('admin_login_page')


@require_POST
def post_config(request):
    form = UserForm(request.POST)
    context = {field: request.POST.get(field) for field in ['email', 'name', 'phone_number', 'brand_name', 'password']}
    
    if form.is_valid():
        # Form data is valid, save the user
        
        user=form.save(commit=False)
        user.name=user.name.lower()
        user.username=user.name 
        user.is_staff=True
        user.brand_name=user.brand_name.lower()
        user.save()
        login(request,user)
        # print('rev:' +reverse('admin_index') + '?success=true')
        # Return JSON response with redirect URL
        to_admin_panel=reverse('admin_index') + '?success=true'
        # Return JSON response with redirect header
        response = JsonResponse({'success': True})
        response['HX-Redirect'] =to_admin_panel
        return response 
    else:
        # Form data is invalid, collect errors
        errors = {f'err_{field}': error_list[0] for field, error_list in form.errors.items()}
          # 'err_'field because eachfied is accessible by the field name to display its value
            # am adding err to the field ,example err_email so that it doesnt conflict with the email's value
               # Include brand_name in the context

        # Merge errors into context
        context.update(errors)

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
    print(request.POST)
    print('request.POST3)')
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