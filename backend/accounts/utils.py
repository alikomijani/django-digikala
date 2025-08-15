import random
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

from accounts.models import OTP


def generate_otp(user):
    code = str(random.randint(100000, 999999))  # 6-digit OTP
    otp = OTP.objects.create(
        user=user, code=code, expires_at=timezone.now() + timedelta(minutes=5)
    )
    # Here, integrate SMS or Email sending
    send_otp_via_sms(user.phone_number, code)
    return otp.session_id


def send_otp_via_sms(phone, code):
    # Integrate Twilio, Kavenegar, or other SMS provider
    print(f"Sending OTP {code} to {phone}")


def verify_otp(user, code, session_id):
    """
    Verify OTP for user and session.
    Returns the OTP instance if valid.
    Raises ValidationError if OTP is invalid, used, or expired.
    """
    try:
        otp = OTP.objects.get(
            user=user, code=code, session_id=session_id, is_used=False
        )
    except OTP.DoesNotExist:
        raise ValidationError("Invalid OTP code.")

    if otp.is_expired():
        raise ValidationError("OTP has expired.")

    return otp
