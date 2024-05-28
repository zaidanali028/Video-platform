from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from ..models import User
from django.http import HttpResponse



@login_required(login_url='admin_login')    
def admin_index(request):
   request.session['page'] = 'Admin Dashboard'
   staff_count = User.objects.filter(is_staff=True, is_active=True).count()
   if staff_count<2:
        # super super admin and the admin using the platform,will take admin to config_platform incase the staff accounts aint 2
        return redirect('config_platform')
   success = request.GET.get('success', False)
   context={"success":success}
   return render(request,'admin_app/pages/admin_index.html',context)

@login_required(login_url='admin_login')    
def admin_genres(request):
   request.session['page'] = 'Admin Genres'
   staff_count = User.objects.filter(is_staff=True, is_active=True).count()
   if staff_count<2:
        # super super admin and the admin using the platform,will take admin to config_platform incase the staff accounts aint 2
        return redirect('config_platform')
   context={}
   return render(request,'admin_app/pages/admin_genres.html',context)




def admin_videos(request):
   request.session['page'] = 'Admin Videos'
   staff_count = User.objects.filter(is_staff=True, is_active=True).count()
   if staff_count<2:
        # super super admin and the admin using the platform,will take admin to config_platform incase the staff accounts aint 2
        return redirect('config_platform')
   context={}
   return render(request,'admin_app/pages/admin_videos.html',context)

