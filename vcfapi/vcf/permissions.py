from rest_framework import permissions

class UserPermissions(permissions.BasePermission):

    # not_user_actions = ['assign_driver', 'stats', 'onboard',
    #                     'activate', 'deactivate', 'update_pricing_model', 'toggle_trip_tracking']

    # disabled user can't create business profile no more 
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # if view.action not in self.not_user_actions:
                return True
        return False

    def has_object_permission(self, request, view, object):
        # if view.action in self.not_user_actions:
        #     return False
        if request.user == object.user:
            return True
        return False

class AdminPermissions(permissions.BasePermission):

    # not_user_actions = ['assign_driver', 'stats', 'onboard',
    #                     'activate', 'deactivate', 'update_pricing_model', 'toggle_trip_tracking']

    # disabled user can't create business profile no more 
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # if view.action not in self.not_user_actions:
                return True
        return False

    def has_object_permission(self, request, view, object):
        # if view.action in self.not_user_actions:
        #     return False
        if request.user.is_staff and 'admin' in request.headers:
            return True
        return False
