from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.basename == "user":
            return bool(request.user.id == obj.id)
        if view.basename in [
            "project",
            "webmaster",
            "contact",
            "messages",
            "payment",
            "payment-history",
            "publish-pages",
            "url",
            "mail",
        ]:
            return bool(request.user.id == obj.owner.id)
        return False

    def has_permission(self, request, view):
        basenames = [
            "auth-logout",
            "user",
            "project",
            "webmaster",
            "contact",
            "messages",
            "payment",
            "payment-history",
            "publish-pages",
            "url",
            "mail",
        ]

        if view.basename in basenames:
            if not request.user.is_anonymous:
                return bool(request.user and request.user.is_authenticated)
        return False
