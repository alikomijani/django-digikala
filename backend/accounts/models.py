import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail

# Optional: for better mobile number handling (pip install django-phonenumber-field)
# from phonenumber_field.modelfields import PhoneNumberField

MOBILE_MAX_LENGTH = 11
NAME_MAX_LENGTH = 150


class UserManager(BaseUserManager):
    """Custom user manager where mobile is the unique identifier."""

    def _create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError("The mobile number must be set")

        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)  # safer than make_password
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        """Create and return a regular user."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields["is_staff"] is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields["is_superuser"] is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(mobile, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model using mobile as the primary identifier."""

    mobile = models.CharField(
        _("mobile number"),
        max_length=MOBILE_MAX_LENGTH,
        unique=True,
    )
    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)
    first_name = models.CharField(
        _("first name"), max_length=NAME_MAX_LENGTH, blank=True
    )
    last_name = models.CharField(_("last name"), max_length=NAME_MAX_LENGTH, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Can log into the admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []  # Django requires this for createsuperuser

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)  # type: ignore

    def get_full_name(self):
        """Return the first name plus the last name."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name or self.mobile

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user if they have one."""
        if not self.email:
            return None
        send_mail(subject, message, from_email, [self.email], **kwargs)


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at
