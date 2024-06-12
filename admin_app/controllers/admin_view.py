from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from ..models import User
from django.http import HttpResponse
from custom_decorators.admin.decorators import staff_required,ensure_platform_configured
from admin_app.services import AppConfig






@staff_required
@ensure_platform_configured 
def admin_index(request):

   request.session['page'] = 'Admin Dashboard'
   user_with_brand = AppConfig.Ownership.get_owner()
   site_name = user_with_brand.brand_name if user_with_brand else None
   site_logo = user_with_brand.brand_image_url if user_with_brand else None
   success = request.GET.get('success', False)
   context={
      "success":success,
      "site_name":site_name,
      "site_logo":site_logo
      }  
   return render(request,'admin_app/pages/admin_index.html',context)


