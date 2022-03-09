from django.contrib import admin
from community.models import Community
from django.contrib.auth.admin import GroupAdmin


class CommunityAdmin(GroupAdmin):
    list_display = ('community_name', 'type', 'zip_code')
    search_fields = ('community_name', 'type')
    readonly_fields = ()
    ordering = ('community_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Community, CommunityAdmin)
