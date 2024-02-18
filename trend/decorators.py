from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

from django.contrib import messages

# if our decorator do not need arguments then we can simply skip the parent function
# Suppose only ADMIN is allowed to visit the page then:
def admin_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, f'You have to login first!')
            return redirect('core:login')
    return wrap