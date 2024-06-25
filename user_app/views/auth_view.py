
from django.http import HttpResponse
from admin_app.models import Category,Genre,User
from django.shortcuts import render,redirect
from django.db.models import Count
from admin_app.Forms.config_platform.Forms import UserForm
from user_app.Forms.auth.Forms import LoginForm,ResetPasswordForm,ConfirmResetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from admin_app.services import Mailer,AppConfig
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import authenticate,login,logout
from custom_decorators.user.decorators import redirect_authenticated


@redirect_authenticated
def registration_page(request):
   
   request.session['page'] = 'Registration'
  
   user_with_brand = AppConfig.Ownership.get_owner()
   
   site_name = user_with_brand.brand_name if user_with_brand else None
   site_logo = user_with_brand.brand_image_url if user_with_brand else None
   genres = Genre.objects.filter(status='active').annotate(genre_count=Count('genres_set')).filter(genre_count__gt=0).order_by('-created_at')[:5]
   categories = Category.objects.filter(status='active').annotate(show_count=Count('categories_set')).filter(show_count__gt=0).order_by('-created_at')[:5]
   password=None
   confirm_password=None
   
   if request.method == 'POST':
      
      
      current_site = get_current_site(request)
      
      changed_data=request.POST.copy()
      if changed_data['password']:
         password=changed_data['password']
      if changed_data['confirm_password']:
         confirm_password=changed_data['confirm_password']
      changed_data['brand_name']="_"
      changed_data["brand_image_url"]=current_site
      form = UserForm(data=changed_data)
    

      
      if form.is_valid():
         
         user=form.save(commit=False)
         
         user.set_password(form.cleaned_data['password'])
         user.username=user.name 
         user.is_active=False
         
         
         user.save()
         # send welcome email
         mailer=Mailer.Mailer()
         mailer.send_welcome_email(user)
         mailer.send_email_confirmation(request,user,'user_app/emails/confirmation.html')
         response = JsonResponse({'success': True})
         to_indexpage=reverse('index_page') + '?created=true'
         response['HX-Redirect'] =to_indexpage
         return response
         
       
         
         
      
      context={'site_name':site_name,'site_logo':site_logo,'categories':categories,'genres':genres,'form':form,'password':password,'confirm_password':confirm_password}
      
      # print(form.errors.items())
      return render(request,'user_app/partials/form_elements/user/registration_form.html',context)
      
      
      
   form = UserForm()
   
   context={'site_name':site_name,'site_logo':site_logo,'categories':categories,'genres':genres,'form':form}
   
   return render(request,'user_app/pages/user/registration.html',context)
   
   
 
def activate_user(request, uidb64, token):
   # Your logic for activating the user
   try:
      uid = urlsafe_base64_decode(uidb64).decode()
      user = User.objects.get(pk=uid)
   except (TypeError, ValueError, User.DoesNotExist):
      user = None
      return HttpResponse("Something aint ok.")
        


   if user is not None and token_generator.check_token(user, token):
      user.is_active = True
      user.save()
      login(request, user)
      response = JsonResponse({'success': True})
      to_indexpage=reverse('index_page') + '?activated=true'
      return redirect(to_indexpage)
     
   else:
      to_indexpage=reverse('index_page') + '?activated=false'
      return redirect(to_indexpage)


def password_reset_confirm(request, uidb64, token) -> HttpResponse:
   request.session['page'] = 'Forgot Password'
   user_with_brand = AppConfig.Ownership.get_owner()
   
   site_name = user_with_brand.brand_name if user_with_brand else None
   site_logo = user_with_brand.brand_image_url if user_with_brand else None
   genres = Genre.objects.filter(status='active').annotate(genre_count=Count('genres_set')).filter(genre_count__gt=0).order_by('-created_at')[:5]
   categories = Category.objects.filter(status='active').annotate(show_count=Count('categories_set')).filter(show_count__gt=0).order_by('-created_at')[:5]
   
    # Your logic for activating the user
   try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
   except (TypeError, ValueError, User.DoesNotExist):
        user = None
        return HttpResponse("Something aint ok.")
        


   if user is not None and token_generator.check_token(user, token):
      # validate user identity and token
            if request.method == 'POST':
               # handle post request after validation if user sends a post req.
               changed_data=request.POST.copy()
               form=ConfirmResetPasswordForm(data=changed_data)
               if form.is_valid():
                  user.set_password(form.cleaned_data['password'])
                  user.save()
                  # relog user in to prevent losing session
                  login(request,user)
                  
                  response = JsonResponse({'success': True})
                  to_indexpage=reverse('index_page') + '?updated=true'
                  response['HX-Redirect'] =to_indexpage
                  return response
               
                  
                  
               # valid token and user  but validation failed
               
               context={'site_name':site_name,'site_logo':site_logo,'categories':categories,'genres':genres,'form':form}
               return render(request,'user_app/partials/form_elements/user/update_password_form.html',context)
               
         
            # valid token and user 
            form=ConfirmResetPasswordForm()
            context={'site_name':site_name,'site_logo':site_logo,'categories':categories,'genres':genres,'form':form}
            return render(request,'user_app/pages/user/update_password.html',context)
       
   else:
      to_indexpage=reverse('index_page') + '?activated=false'
      return redirect(to_indexpage)

@redirect_authenticated
def forgot_password_page(request):
   request.session['page'] = 'Forgot Password'
  
   user_with_brand = AppConfig.Ownership.get_owner()
   
   site_name = user_with_brand.brand_name if user_with_brand else None
   site_logo = user_with_brand.brand_image_url if user_with_brand else None
   genres = Genre.objects.filter(status='active').annotate(genre_count=Count('genres_set')).filter(genre_count__gt=0).order_by('-created_at')[:5]
   categories = Category.objects.filter(status='active').annotate(show_count=Count('categories_set')).filter(show_count__gt=0).order_by('-created_at')[:5]
   
   if request.method == 'POST':
      changed_data=request.POST.copy()
      form = ResetPasswordForm(data=changed_data)
      
      if form.is_valid():
         form_email=form.cleaned_data.get('email')
         # send reset email
         mailer=Mailer.Mailer()
         user=User.objects.filter(email=form_email).first()
         mailer.send_forgot_password_email(request,user,'user_app/emails/reset_password.html')
         response = JsonResponse({'success': True})
         to_indexpage=reverse('index_page') + '?reset=true'
         response['HX-Redirect'] =to_indexpage
         return response
         
            # form.add_error('password','Wrong Credentials Provided!')
      context={'site_name':site_name,'site_logo':site_logo,'categories':categories,'genres':genres,'form':form}
      
      return render(request,'user_app/partials/form_elements/user/forgot_password_form.html',context)
         
   
   form = ResetPasswordForm()
   


   context={'site_name':site_name,'site_logo':site_logo,'categories':categories,'genres':genres,'form':form}

   return render(request,'user_app/pages/user/forgot_password.html',context)


   
   
@redirect_authenticated
def login_page(request):
   request.session['page'] = 'Login'
  
   user_with_brand = AppConfig.Ownership.get_owner()
   
   site_name = user_with_brand.brand_name if user_with_brand else None
   site_logo = user_with_brand.brand_image_url if user_with_brand else None
   genres = Genre.objects.filter(status='active').annotate(genre_count=Count('genres_set')).filter(genre_count__gt=0).order_by('-created_at')[:5]
   categories = Category.objects.filter(status='active').annotate(show_count=Count('categories_set')).filter(show_count__gt=0).order_by('-created_at')[:5]
   password=None
   
   if request.method == 'POST':
      form_data=request.POST
      if form_data['password']:
         password=form_data['password']
      
      form = LoginForm(data=form_data)
      
      if form.is_valid():
         form_email=form.cleaned_data.get('email')
         form_ppassword=form.cleaned_data.get('password')
         user_auth=authenticate(request,email=form_email,password=form_ppassword)

         if user_auth is not None:
            login(request,user_auth)
            response = JsonResponse({'success': True})
            to_indexpage=reverse('index_page') + '?authenticated=true'
            response['HX-Redirect'] =to_indexpage
            return response
         else:
            form.add_error('password','Wrong Credentials Provided!')
      context={'site_name':site_name,'site_logo':site_logo,'categories':categories,'genres':genres,'form':form,'password':password,}
      
      return render(request,'user_app/partials/form_elements/user/login_form.html',context)
         
   
   form = LoginForm()
   


   context={'site_name':site_name,'site_logo':site_logo,'categories':categories,'genres':genres,'form':form,'password':password,}

   return render(request,'user_app/pages/user/login.html',context)




def logout_page(request):
   logout(request)
   to_indexpage=reverse('login_page') + '?authenticated=false'
   return redirect(to_indexpage)