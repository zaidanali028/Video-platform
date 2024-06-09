
from django.http import HttpResponse
from admin_app.models import Category,Genre,User
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from time import sleep
from django.db.models import Count
from admin_app.Forms.config_platform.Forms import UserForm
from django.contrib.sites.shortcuts import get_current_site
from admin_app.services import Mailer,AppConfig
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.http import HttpRequest
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import login

   
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
      
      print(form.errors.items())
      return render(request,'user_app/partials/form_elements/user/registration_form.html',context)
      
      
      
   form = UserForm()
   
   context={'site_name':site_name,'site_logo':site_logo,'categories':categories,'genres':genres,'form':form}
   
   return render(request,'user_app/pages/user/register.html',context)
   
   
   
def activate_user(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
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
      response = JsonResponse({'success': True})
      to_indexpage=reverse('index_page') + '?activated=false'
      return redirect(to_indexpage)