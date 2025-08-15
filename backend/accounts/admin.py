from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User, OTP


class OTPInline(admin.TabularInline):
    model = OTP
    extra = 0
    readonly_fields = ["code", "session_id", "created_at", "expires_at", "is_used"]
    can_delete = False


class UserAdmin(BaseUserAdmin):
    list_display = [
        "mobile",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    ]
    ordering = ["mobile"]
    search_fields = ["mobile", "email", "first_name", "last_name"]
    readonly_fields = ["date_joined", "last_login"]

    fieldsets = (
        (None, {"fields": ("mobile", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("mobile", "email", "password1", "password2"),
            },
        ),
    )

    inlines = [OTPInline]


admin.site.register(User, UserAdmin)
