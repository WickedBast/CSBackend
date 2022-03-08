from django.contrib import admin
from community.models import Community
from django.contrib.auth.admin import UserAdmin


class CommunityAdmin(UserAdmin):
    list_display = ('community_name', 'type', 'zip_code')
    search_fields = ('community_name', 'type')
    readonly_fields = ('community_name', )
    ordering = ('community_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Community, CommunityAdmin)
