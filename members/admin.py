from django.contrib import admin
from members.models import Member
from django.contrib.auth.admin import GroupAdmin


class MemberAdmin(GroupAdmin):
    list_display = ('organization_name', 'first_name', 'last_name', 'type', 'nip_number')
    search_fields = ('organization_name',)
    readonly_fields = ()
    ordering = ('organization_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Member, MemberAdmin)
