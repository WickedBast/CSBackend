from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from communities.models import Community, CommunityUsers


class UserInline(admin.TabularInline):
    model = CommunityUsers
    raw_id_fields = ['users']


class CommunityAdmin(GroupAdmin):
    list_display = ('name', 'type', 'zip_code')
    search_fields = ('name', 'type')
    readonly_fields = ()
    ordering = ('name',)

    inlines = (UserInline, )
    filter_horizontal = ()
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('type',)}),
        ('Community Information', {'fields': ('name', 'phone_number')}),
        ('Address Information', {'fields': ('zip_code', 'address', 'city')}),
    )


admin.site.register(Community, CommunityAdmin)
