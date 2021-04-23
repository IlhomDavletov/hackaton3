from django.core.mail import send_mail

def send_activation_email(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    message = f'Thank you for registration!\nTo activate your account, please click link here {activation_url}'
    send_mail(
        'First step to finding your love is done!', message, 'admin@admin.com', [email,], fail_silently=False
    )
