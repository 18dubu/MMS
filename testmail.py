from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

print 'pass1'
send_mail('header3', 'body2', settings.EMAIL_HOST_USER, ['handong.ma@pfizer.com'], fail_silently=False)
print 'pass2'

email = EmailMessage('Mail Test', 'This is a test', to=['handong.ma@pfizer.com'])
email.send()
print 'done'
