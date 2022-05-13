import sweetify
from django.shortcuts import redirect


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.first().name
                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    sweetify.error(request, title="ERROR", text="YOU ARE NOT AUTHORIZED ", icon="error")
                    return redirect('home')

        return wrapper_func

    return decorator
