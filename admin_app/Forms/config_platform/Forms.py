# forms.py
from django import forms
from django.core.validators import EmailValidator
from admin_app.models  import User
from django.core.validators import  RegexValidator

class EmailValidationForm(forms.Form):
    email = forms.CharField(max_length=254, validators=[EmailValidator()])

    def unique_email(self):
        
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            return False
        return True
    
class NameValidationForm(forms.Form):
    name = forms.CharField(max_length=255)

    def unique_name(self):
        name = self.cleaned_data.get('name').lower()
        if User.objects.filter(name=name).exists():
            return False
        return True
    

class PhoneNumberValidationForm(forms.Form):
    phone_number = forms.CharField(min_length=10)

    def unique_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            return False
        return True

class BrandNameValidationForm(forms.Form):
    brand_name = forms.CharField(max_length=255)

    def unique_brand_name(self):
        brand_name = self.cleaned_data.get('brand_name').lower()
        if User.objects.filter(brand_name=brand_name).exists():
            return False
        return True

    
class PasswordChangeForm(forms.Form):
    password = forms.CharField(
        min_length=10,
        validators=[
            # MinLengthValidator(10, message='Password must be at least 10 characters long'),
            RegexValidator(
                regex='^(?=.*\d)(?=.*[a-zA-Z]).{10,}$',  # Requires at least one digit and one letter
                message='Password must contain at least one digit and one letter',
                code='invalid_password'
            )
        ],
       
    )
    def password_match(self, password,confirm_password):
        
        if password != confirm_password:
            return False
        return True
    

# a form for the User model
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone_number', 'brand_name', 'password','brand_image_url']
        # exclude=['*']

    password = forms.CharField(
        min_length=10,
        validators=[
            RegexValidator(
                regex='^(?=.*\d)(?=.*[a-zA-Z]).{10,}$',  # Requires at least one digit and one letter
                message='Password must contain at least one digit and one letter',
            )
        ],
      
    )
    confirm_password = forms.CharField(
        min_length=10,
        
       
    )

# overwriting some validation fields from the Form
  
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match (:')
        return confirm_password
    
    
    
    
    def clean_brand_image_url(self):
        brand_image_url = self.cleaned_data.get('brand_image_url')
        if  brand_image_url is  None:
            raise forms.ValidationError("A brand_image is required")
        return brand_image_url
    