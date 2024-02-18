from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

class UserIsAdmin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('core:login')