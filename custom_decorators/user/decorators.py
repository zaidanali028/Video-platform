from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

un_restricted_routes = [
    # must be a named route

    'login_page',
    'registration_page',
    'forgot_password_page'

]

# a decorator function to redirect auth users from unauthenticated routes
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





def ensure_auth(view_func):
    """
    Decorator to ensure the user is authenticated.
    Redirects to the login page with an error message if the user is not logged in.
    If authenticated, proceeds to the original view.
    
    Args:
        view_func (function): The view function to wrap.
        
    Returns:
        function: The wrapped view function.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Add an error message and redirect to the login page
            messages.error(request, 'Please login to access this resource!')
            return redirect('login_page')
        
        # If authenticated, call the original view function
        return view_func(request, *args, **kwargs)

    return _wrapped_view
