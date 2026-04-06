# from rest_framework import permissions
#
#
# class IsAuthorOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission: Only the author of an object can edit/delete it.
#     Everyone can read (GET, HEAD, OPTIONS).
#
#     - has_object_permission checks if request.method is safe OR obj.author == request.user
#     """
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         return obj.author == request.user
#

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Tizimga kirmagan foydalanuvchilar faqat o'qiy oladi (GET)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Yaratish (POST) uchun foydalanuvchi tizimga kirgan bo'lishi shart
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS (GET, HEAD, OPTIONS) hamma uchun ochiq
        if request.method in permissions.SAFE_METHODS:
            return True

        # O'zgartirish va o'chirish faqat muallifga ruxsat
        return obj.author == request.user
