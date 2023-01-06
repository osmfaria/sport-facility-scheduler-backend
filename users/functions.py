from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .token import AccountActivationTokenGenerator
from django.utils.html import strip_tags
from django.core import mail
from project import settings


account_activation_token = AccountActivationTokenGenerator()

def sendActivateEmail(request, user, recipient):
    subject = 'Activate your user account.'
    link = f"http://{get_current_site(request).domain}/api/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}/"
    
    message = render_to_string('welcome.html', {
        'user': user,
        'link':link,
        'protocol': 'https' if request.is_secure() else 'http'
    })

    text_content = strip_tags(message)

    email = mail.EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, recipient)
    email.attach_alternative(message, "text/html")
    email.send()


   
