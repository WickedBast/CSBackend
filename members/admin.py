from django.contrib import admin
from members.models import Member
from users.models import User
from django.contrib.auth.admin import GroupAdmin


class UserInline(admin.TabularInline):
    model = User
    fields = ('email',)
    raw_id_fields = ['member']
    extra = 0


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
        ('Community', {'fields': ('communities',)})
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
        ('Community', {'fields': ('communities',)})
    )

    inlines = (UserInline,)

    filter_horizontal = ()
    list_filter = ()


admin.site.register(Member, MemberAdmin)
