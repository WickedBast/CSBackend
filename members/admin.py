from django.contrib import admin
from members.models import Member
from django.contrib.auth.admin import UserAdmin


class MemberAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'organization_name', 'type', 'nip_number')
    search_fields = ('organization_name',)
    readonly_fields = ('first_name', 'last_name')
    ordering = ('organization_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Member, MemberAdmin)
