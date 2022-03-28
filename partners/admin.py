from django.contrib import admin
from partners.models import Partner, PartnerUsers
from django.contrib.auth.admin import GroupAdmin


class UserInline(admin.TabularInline):
    model = PartnerUsers
    raw_id_fields = ['users']


class PartnerAdmin(GroupAdmin):
    list_display = ('name', 'type', 'partner_type', 'phone_number', 'nip_number')
    search_fields = ('name',)
    readonly_fields = ()
    ordering = ('name',)

    fieldsets = (
        (None, {'fields': ('type',)}),
        ('Partner Information', {'fields': ('name', 'partner_type', 'phone_number', 'nip_number', 'energy_tariff')}),
        ('Address Information', {'fields': ('zip_code', 'address', 'city')}),
        ('Photovoltaic Fields', {'fields': (
            'pv_technology', 'pv_power_peak_installed', 'system_loss', 'mounting_position', 'slope', 'azimuth'
        )}),
        ('Community', {'fields': ('communities',)}),
    )

    inlines = (UserInline,)
    filter_horizontal = ('communities',)
    list_filter = ()


admin.site.register(Partner, PartnerAdmin)
