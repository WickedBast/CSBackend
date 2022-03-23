from django.contrib import admin
from members.models import Member, MemberUsers
from django.contrib.auth.admin import GroupAdmin


class UserInline(admin.TabularInline):
    model = MemberUsers
    raw_id_fields = ['users']


class MemberAdmin(GroupAdmin):
    list_display = ('type', 'first_name', 'last_name', 'organization_name', 'nip_number')
    search_fields = ('organization_name', 'nip_number', 'first_name', 'last_name')
    readonly_fields = ()
    ordering = ('type',)

    fieldsets = (
        (None, {'fields': ('type', 'phone_number', 'energy_tariff')}),
        ('Personal Information', {'fields': ('first_name', 'last_name')}),
        ('Organization Information', {'fields': ('organization_name', 'nip_number')}),
        ('Address Information', {'fields': ('zip_code', 'address', 'city')}),
        ('Photovoltaic Fields', {'fields': (
            'pv_technology', 'pv_power_peak_installed', 'system_loss', 'mounting_position', 'slope', 'azimuth'
        )}),
        ('Community', {'fields': ('community',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'type', 'phone_number', 'energy_tariff'
            )
        }),
        ('Personal Information', {'fields': ('first_name', 'last_name')}),
        ('Organization Information', {'fields': ('organization_name', 'nip_number')}),
        ('Address Information', {'fields': ('zip_code', 'address', 'city')}),
        ('Photovoltaic Fields', {'fields': (
            'pv_technology', 'pv_power_peak_installed', 'system_loss', 'mounting_position', 'slope', 'azimuth'
        )}),
        ('Community', {'fields': ('community',)})
    )

    inlines = (UserInline, )
    filter_horizontal = ()
    list_filter = ()


admin.site.register(Member, MemberAdmin)
