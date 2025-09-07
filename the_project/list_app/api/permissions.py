from rest_framework import permissions

# custom permissions: https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        #ver si la persona es usuario y si tiene staff status
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)
    
class IsReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):    
        # SAFE_METHOD se refiere solo a GET
        if request.method in permissions.SAFE_METHODS:
    # Check permissions for read-only request
            return True

    #si no es SAFE_METHOD, como POST, DELETE, etc
        else:
    # Check permissions for write request, i.e. admin == usuario
            return obj.review_user == request.user or request.user.is_staff