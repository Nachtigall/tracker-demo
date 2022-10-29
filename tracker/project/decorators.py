from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from .models import Project


def check_ownership(func):
    """
    Make sure that only project owner is able to edit projects.
    """

    @wraps(func)
    def wrapper(view, request, *args, **kwargs):
        if request.user.id == Project.objects.get(pk=kwargs["pk"]).project_owner_id:
            return func(view, request, *args, **kwargs)
        else:
            return Response(
                "Only project owners are allowed to perform changes.",
                status=status.HTTP_403_FORBIDDEN,
            )

    return wrapper
