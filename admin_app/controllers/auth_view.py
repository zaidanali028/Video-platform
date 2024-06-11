
from django.http import HttpResponse
from ..models import User
from admin_app.services import AppConfig


def admin_login(request):
    request.session['page'] = 'Admin Login'

    return HttpResponse('admin_login_page')
