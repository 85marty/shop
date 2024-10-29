from functools import wraps

from django.http import HttpResponseForbidden, request


def group_required(group_name, request):
    return request.user.is_authenticated and request.user.groups.filter(name=group_name).exists()


def group_required_decorator(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if group_required(group_name, request):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()

        return _wrapped_view

    return decorator
