from django import forms
from django.core.validators import EmailValidator
from admin_app.models  import User
from django.core.validators import  RegexValidator

class LoginForm(forms.Form):
    email = forms.CharField(max_length=254, validators=[EmailValidator()])
    password = forms.CharField(
        min_length=10,
        validators=[
            RegexValidator(
                regex='^(?=.*\d)(?=.*[a-zA-Z]).{10,}$',  # Requires at least one digit and one letter
                message='Password must contain at least one digit and one letter',
            )
        ],
      
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            return email
            
        raise forms.ValidationError('Email Does Not Exist!')
            


class ResetPasswordForm(forms.Form):
    email = forms.CharField(max_length=254, validators=[EmailValidator()])
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            return email
            
        raise forms.ValidationError('Email Does Not Exist!')
    
    

class ConfirmResetPasswordForm(forms.Form):
    password = forms.CharField(
        min_length=10,
        validators=[
            # MinLengthValidator(10, message='Password must be at least 10 characters long'),
            RegexValidator(
                regex='^(?=.*\d)(?=.*[a-zA-Z]).{10,}$',  # Requires at least one digit and one letter
                message='Password must contain at least one digit and one letter',
            )
        ],
       
    )
    confirm_password = forms.CharField(
        min_length=10,
        validators=[
            # MinLengthValidator(10, message='Password must be at least 10 characters long'),
            RegexValidator(
                regex='^(?=.*\d)(?=.*[a-zA-Z]).{10,}$',  # Requires at least one digit and one letter
                message='Password must contain at least one digit and one letter',
            )
        ],
       
    )
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match (:')
        return confirm_password
