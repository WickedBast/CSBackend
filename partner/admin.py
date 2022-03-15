from django.contrib import admin
from partner.models import Partner
from users.models import User
from django.contrib.auth.admin import GroupAdmin


class UserInline(admin.TabularInline):
    model = User
    raw_id_fields = ['partner']
    exclude = ('community', 'member', 'password', 'types', 'is_admin', 'is_active', 'is_staff', 'is_superuser')


class PartnerAdmin(GroupAdmin):
    list_display = ('partner_name', 'type', 'partner_type', 'phone_number', 'nip_number')
    search_fields = ('partner_name',)
    readonly_fields = ()
    ordering = ('partner_name',)

    fieldsets = (
        (None, {'fields': ('type',)}),
        ('Partner Information', {'fields': ('partner_name', 'partner_type', 'phone_number', 'nip_number', 'zip_code')}),
        ('Community', {'fields': ('community',)})
    )

    inlines = (UserInline,)

    filter_horizontal = ()
    list_filter = ()


admin.site.register(Partner, PartnerAdmin)
