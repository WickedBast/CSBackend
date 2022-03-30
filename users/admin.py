from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin


class UsersAdmin(UserAdmin):
    list_display = (
        'email', 'types', 'date_joined', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser'
    )
    list_filter = (
        'email', 'date_joined', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser'
    )
    fieldsets = (
        (None, {'fields': ('types',)}),
        ('Credentials', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
        ('Token', {'fields': ('token',)})
    )
    add_fieldsets = (
        (None, {'fields': ('types',)}),
        ('Credentials', {'fields': ('email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UsersAdmin)
