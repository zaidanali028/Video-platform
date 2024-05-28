
from django.http import HttpResponse
from ..models import User


def admin_login(request):
    request.session['page'] = 'Admin Login'

    return HttpResponse('admin_login_page')
