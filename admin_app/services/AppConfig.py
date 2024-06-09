# This  file  handles the authenticity/ site ownership of this platform
from admin_app.models import User

class Ownership:
    
    # method to return the user that is a valid super admin
    @staticmethod
    def get_owner():
        user_with_brand = User.objects.filter(brand_name__isnull=False,brand_image_url__isnull=False,is_staff=True).first()
        return user_with_brand
    
        