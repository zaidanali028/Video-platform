
from django.http import HttpResponse
from ..models import User
from admin_app.services import AppConfig
from custom_decorators.admin.decorators import staff_required,ensure_platform_configured
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from admin_app.Forms.auth.Forms import UpdatePasswordForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from admin_app.Forms.auth.Forms import LoginForm
from custom_decorators.admin.decorators import redirect_authenticated
from time import sleep

@redirect_authenticated
def admin_login(request):
    request.session['page'] = 'Admin Login'
    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    if request.method=='POST':

        form_data=request.POST
        form = LoginForm(data=form_data)
        if form.is_valid():
            form_email=form.cleaned_data.get('email')
            form_password=form.cleaned_data.get('password')
            print(form_email,form_password)

            user_auth=authenticate(request,email=form_email,password=form_password)
            print('user_auth')
            print(user_auth)

            if user_auth is not None:
                login(request,user_auth)
                response = JsonResponse({'success': True})
                to_indexpage=reverse('admin_index') + '?authenticated=true'
                response['HX-Redirect'] =to_indexpage
                return response
            else:
                form.add_error('password','Wrong Credentials Provided!')
  
        return render(request, 'admin_app/partials/form_elements/auth/login_form.html', {
                        'form':form,
                        'site_name':site_name,
                        'site_logo':site_logo,
                        })

    
    
    form=LoginForm()
    return render(request, 'admin_app/pages/auth/login.html',{
        'form':form,
        'site_name':site_name,
        'site_logo':site_logo,
        })
    # return HttpResponse('admin_login_page')
    return

@staff_required
@ensure_platform_configured 
def admin_update_password(request):
    request.session['page'] = 'Admin Password Update'

    user_with_brand = AppConfig.Ownership.get_owner()
    site_name = user_with_brand.brand_name if user_with_brand else None
    site_logo = user_with_brand.brand_image_url if user_with_brand else None
    user = request.user
    password=None
    confirm_password=None

    if request.method == 'POST':
        # Make POST data mutable to manipulate it
      
        form_data = request.POST.copy()
        # print('form_data')
        # print(form_data)
        if form_data['password']:
           password=form_data['password']

        if form_data['confirm_password']:
           confirm_password=form_data['confirm_password']

        
        form = UpdatePasswordForm(data=form_data)
        if form.is_valid():
            if form_data['old_password']:
                user_auth=authenticate(request,email=request.user.email,password=form_data['old_password'])
                if user_auth is  None:
                    form.add_error('password', 'Old Password is wrong.')
                    form.add_error('confirm_password', 'Old Password is wrong.')
                    return render(request, 'admin_app/partials/form_elements/auth/update_password_form.html', {
                        'form': form,
                        'site_name': site_name,
                        'site_logo': site_logo,
                        'password': password,
                        'confirm_password': confirm_password
        })
                else:
                    # encrypt password before saving
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    # maintain user's session and dont log user out after password update
                    login(request,user)
                    response = JsonResponse({'success': True})
                    to_admin_panel=reverse('admin_index') + '?updated=true'
                    response['HX-Redirect'] =to_admin_panel
                    return response 

        
        
        # re-render the form fields with validation errors and other data

        else:
            return render(request, 'admin_app/partials/form_elements/auth/update_password_form.html',{
                'form':form,
                'site_name':site_name,
                'site_logo':site_logo,
                'password':password,
                'confirm_password':confirm_password
        })
 

            

    
    form = UpdatePasswordForm()
    return render(request, 'admin_app/pages/auth/update_password.html',{
        'form':form,
        'site_name':site_name,
        'site_logo':site_logo,
        'password':password,
        'confirm_password':confirm_password
        })



def admin_logout(request):
 
    logout(request)
    to_indexpage=reverse('admin_login') + '?authenticated=false'
    return redirect(to_indexpage)