from django.contrib import admin
from members.models import Member
from django.contrib.auth.admin import GroupAdmin


class MemberAdmin(GroupAdmin):
    list_display = ('type', 'first_name', 'last_name','organization_name', 'nip_number')
    search_fields = ('organization_name', 'first_name', 'nip_number')
    readonly_fields = ()
    ordering = ('type',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Member, MemberAdmin)
