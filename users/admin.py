from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin


class UsersAdmin(UserAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'date_joined',
        'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, UsersAdmin)
