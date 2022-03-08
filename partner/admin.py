from django.contrib import admin
from partner.models import Partner
from django.contrib.auth.admin import UserAdmin


class PartnerAdmin(UserAdmin):
    list_display = ('partner_name', 'type', 'partner_type', 'phone_number', 'nip_number')
    search_fields = ('partner_name',)
    readonly_fields = ('partner_name',)
    ordering = ('partner_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Partner, PartnerAdmin)
