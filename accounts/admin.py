from django.contrib import admin
from accounts.models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    pass
