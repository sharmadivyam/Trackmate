from django.contrib import admin
from .models import Task
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

admin.site.register(Task)



User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('username', 'email', 'is_superuser', 'reporting_manager')
    list_filter = ('is_superuser', 'reporting_manager')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ( 'email', 'first_name', 'last_name', 'reporting_manager')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Use built-in password1/password2 fields only for admin "Add User" page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email',  'password1', 'password2', 'reporting_manager'),
        }),
    )

    search_fields = ('username', 'email', 'reporting_manager__username')
    ordering = ('username',)


# Register your models here.
