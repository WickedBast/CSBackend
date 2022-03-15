from django.contrib import admin
from community.models import Community
from members.models import Member
from users.models import User
from django.contrib.auth.admin import GroupAdmin


class MemberInline(admin.TabularInline):
    model = Member
    raw_id_fields = ['community']
    exclude = (
        'type', 'phone_number', 'energy_tariff', 'pv_technology', 'pv_power_peak_installed', 'system_loss',
        'mounting_position', 'slope', 'azimuth'
    )


class UserInline(admin.TabularInline):
    model = User
    raw_id_fields = ['community']
    exclude = ('member', 'partner', 'password', 'types', 'is_admin', 'is_active', 'is_staff', 'is_superuser')


class CommunityAdmin(GroupAdmin):
    list_display = ('community_name', 'type', 'zip_code')
    search_fields = ('community_name', 'type')
    readonly_fields = ()
    ordering = ('community_name',)

    inlines = (MemberInline, UserInline,)

    filter_horizontal = ()
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('type',)}),
        ('Community Information', {'fields': ('community_name', 'zip_code', 'phone_number')}),
    )


admin.site.register(Community, CommunityAdmin)
