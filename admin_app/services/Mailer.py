from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpRequest
from django.contrib.auth.models import User
from admin_app.models  import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator as token_generator
from . import AppConfig

class Mailer:
    def __init__(self):
        user_with_brand=AppConfig.Ownership.get_owner()
        self.user_with_brand=user_with_brand
    def send_welcome_email(self,user: User) -> bool:
        
        """
        Sends a welcome email to the new user.
        :param user: User instance.
        :return: True if email is sent successfully, otherwise False.
        """
        subject = f"Welcome to Our {self.user_with_brand.brand_name} User Registration System"
        message = (
            f"Hello {user.name}!\n\n"
            f"Thank you for registering on our website. "
            f"Please confirm your email address to activate your account.\n\n"
            f"Regards,\nThe {self.user_with_brand.brand_name} Team"
        )
       
        return(self.send_plain_email(
            subject,message,[user.email]
        ))

   # return mailer.send_plain_email(sub, msg, [user.email])
    def send_plain_email(self,subject: str, message: str, recipient_list: list, fail_silently: bool = True) -> bool:

        """
        Sends a plain text email.
        :param subject: Email subject.
        :param message: Email message.
        :param recipient_list: List of email recipients.
        :param fail_silently: Flag to indicate silent fail.
        :return: True if email is sent successfully, otherwise False.
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        try:
            return send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False
            )
            # return True
        except Exception as e:
            print(f"Error sending plain email to {recipient_list}: {e}")  # Replace with error handling if needed
            return False

    def send_html_email(self,subject: str, template_name: str, context: dict, recipient_list: list, fail_silently: bool = True) -> bool:
        """
        Sends an HTML email using a template.
        :param subject: Email subject.
        :param template_name: Template name for the email body.
        :param context: Context for rendering the template.
        :param recipient_list: List of email recipients.
        :param fail_silently: Flag to indicate silent fail.
        :return: True if email is sent successfully, otherwise False.
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        try:
            message_html = render_to_string(template_name, context)
            email = EmailMessage(
                subject=subject,
                body=message_html,
                from_email=from_email,
                to=recipient_list,
            )
            email.content_subtype = "html"  # Specify the email content type as HTML
            email.send(fail_silently=fail_silently)
            return True
        except Exception as e:
            print(f"Error sending HTML email to {recipient_list}: {e}")  # Replace with error handling if needed
            return False

    def send_email_confirmation(self,request: HttpRequest, user: User, template_name: str ) -> bool:
        """
        Sends an email confirmation link to the user.
        :param request: HttpRequest object.
        :param user: User instance.
        :param template_name: Template name for the email body.
        :return: True if email is sent successfully, otherwise False.
        """
    

        current_site = get_current_site(request)
        subject = "Confirm Your Email Address"
        context = {
            'name': user.name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
            'brand_name':self.user_with_brand.brand_name
        }

        return self.send_html_email(subject, template_name, context, [user.email])