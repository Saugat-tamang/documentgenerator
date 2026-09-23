from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from functools import wraps

def permission_required_redirect(perm, redirect_url):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_perm(perm):
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


