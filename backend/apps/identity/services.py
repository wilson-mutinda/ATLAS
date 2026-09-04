from django.contrib.auth import get_user_model, tokens
from django.conf import settings
from django.core.mail import send_mail

User = get_user_model()

def generate_password_reset_token(email):
    user = User.objects.filter(email__iexact=email).first()

    if not user:
        return None

    token = tokens.default_token_generator.make_token(user)

    return {
        "user": user,
        "token": token,
    }

def send_password_reset_email(user, token):
    reset_url = (
        f"{settings.FRONTEND_URL}/reset-password/"
        f"?uid={user.pk}&token={token}"
    )

    subject = "Reset your Atlas password"

    message = f"""
Hello {user.first_name},
We received a request to reset your Atlas Business Suite password.
Use the link below to reset your password.

{reset_url}

If you did not request a password reset, you can safely ignore this email. 
This password-reset link is temporary and should not be shared with anyone.

Regards,
Atlas Business Suite
""".strip()
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
