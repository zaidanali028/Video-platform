from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin-app/', include('admin_app.urls')),
    path('admin/', admin.site.urls),
    path('', include('user_app.urls')),
    

]
