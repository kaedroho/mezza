from functools import wraps

from django.shortcuts import get_object_or_404

from mezza.models import Space


def space(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        space_slug = kwargs.pop("space_slug")
        if space_slug:
            request.space = get_object_or_404(Space, slug=space_slug)
        else:
            request.space = None
        return fn(request, *args, **kwargs)

    return wrapper
