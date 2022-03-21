from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin

from communities.models import Community
from users.models import User


class UserInline(admin.TabularInline):
    model = User
    fields = ('email',)
    raw_id_fields = ['community']
    extra = 0


class CommunityAdmin(GroupAdmin):
    list_display = ('name', 'type', 'zip_code')
    search_fields = ('name', 'type')
    readonly_fields = ()
    ordering = ('name',)

    inlines = (UserInline,)

    filter_horizontal = ()
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('type',)}),
        ('Community Information', {'fields': ('name', 'phone_number')}),
        ('Address Information', {'fields': ('zip_code', 'address', 'city')})
    )


admin.site.register(Community, CommunityAdmin)
