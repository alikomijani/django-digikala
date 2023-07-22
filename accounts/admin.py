from django.contrib import admin
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'mobile',
                    'first_name', 'last_name', 'is_active', ]
    ordering = ['email']
    search_fields = ['mobile', 'email']
    readonly_fields = ['date_joined', 'last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'mobile', 'password1', 'password2')
        }),
    )
    fieldsets = (
        (None, {
            "fields": (
                'email',
                'mobile',
                'password',
            ),
        }),
        (_('Personal info'), {
            "fields": ('first_name', 'last_name', 'balance')
        }),
        (_('Permissions'), {
            "fields": ('is_staff', 'is_active', 'is_superuser',
                       "groups",
                       "user_permissions",
                       )
        }),
        (_('Important dates'), {
            "fields": ('last_login', 'date_joined')
        }),
    )


admin.site.register(User, UserAdmin)
