from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from admin_app.models import User



# a decorator function to confirm if the platform is configured
def ensure_platform_configured(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Get the count of active staff users
        staff_count = User.objects.filter(is_staff=True, is_active=True).count()
        
        if staff_count < 2:
            # Redirect to the configuration page if there are fewer than 2 active staff members
            return redirect('config_platform')
        
        # Call the original view function
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

# a decorator function to confirm the staff status of admins
def staff_required(view_func):
    # the  decorator funcction takes a view's  function  as an arg

    @login_required(login_url='admin_login')
    # ensures the client is logged...

    @wraps(view_func)
    # persists the metadata the vew_func is coming with already


    # _wrapped_view is where I will be implementing my staff check logic
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index_page')
    return _wrapped_view



