from django.contrib import admin
from partners.models import Partner
from users.models import User
from django.contrib.auth.admin import GroupAdmin


class UserInline(admin.TabularInline):
    model = User
    fields = ('email',)
    raw_id_fields = ['partner']
    extra = 0


class PartnerAdmin(GroupAdmin):
    list_display = ('name', 'type', 'partner_type', 'phone_number', 'nip_number')
    search_fields = ('name',)
    readonly_fields = ()
    ordering = ('name',)

    fieldsets = (
        (None, {'fields': ('type',)}),
        ('Partner Information', {'fields': ('name', 'partner_type', 'phone_number', 'nip_number')}),
        ('Address Information', {'fields': ('zip_code', 'address', 'city')}),
        ('Community', {'fields': ('communities',)}),
    )

    inlines = (UserInline,)

    filter_horizontal = ('communities',)
    list_filter = ()


admin.site.register(Partner, PartnerAdmin)
