from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

un_restricted_routes = [
    # must be a naed route

    'login_page',
    'registration_page',
    'forgot_password_page'

]

# a decorator function to redirect auth users from unauthenticated routes8
def redirect_authenticated(view_func):
    # Decorator to redirect authenticated users trying to access restricted routes
    # to their previous page or a default page.
    @wraps(view_func)


    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            current_path = request.path
            
            # Check if the current path is in the list of restricted routes
            for route in un_restricted_routes:
                if current_path == reverse(route):
                    # Redirect to the referrer or default to 'home_page'
                    return redirect(request.META.get('HTTP_REFERER', 'index_page'))
        # Call the original view function
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
