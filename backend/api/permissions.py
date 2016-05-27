from rest_framework import permissions 

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

###########################################################################################
# You can also use IsAuthenticated and IsAdminUser(actually admin or manager) permissions #
# from rest_framework.permissions 														  #	
###########################################################################################

class IsManagerOrReadOnly(permissions.BasePermission):
	def has_permission(self, request, view):
		return (
			(request.user and request.user.is_staff) or
			(request.user and request.user.is_authenticated() and request.method in SAFE_METHODS)
			)

class IsSuperuser(permissions.BasePermission):
	def has_permission(self, request, view):
		return (request.user and request.user.is_superuser)

class IsSuperuserOrReadOnlyManager(permissions.BasePermission):
	def has_permission(self, request, view):
		return (
			(request.user and request.user.is_superuser) or
			(request.user and request.user.is_staff and request.method in SAFE_METHODS)
			)		
			