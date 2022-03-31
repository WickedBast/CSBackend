from rest_framework.permissions import IsAuthenticated, IsAdminUser


class OMixin:
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return super().has_permission(request, view)


class OIsAuthenticated(OMixin, IsAuthenticated): pass


class OIsAdminUser(OMixin, IsAdminUser): pass
