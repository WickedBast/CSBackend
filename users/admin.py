from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin


class UsersAdmin(UserAdmin):
    list_display = (
        'email', 'date_joined','last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser'
    )
    list_filter = (
        'email', 'date_joined', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser'
    )
    fieldsets = (
        (None, {'fields': (
            'email', 'password', 'types', 'community', 'member', 'partner'
        )}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'types', 'password1', 'password2', 'is_admin', 'is_active', 'community', 'member', 'partner'
            )
        }),
    )
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UsersAdmin)
