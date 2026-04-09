from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_active", "is_staff", "birth_date")
    ordering = ("id", )
    fieldsets = (
        (None, {"fields": ("email", "password", "birth_date")}),
        (
            "Permissions",
            {
                "fields" : (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions"
                ),
            },
        ),
        ("Important dates", {"fields" : ("last_login",)}),
    )