from functools import wraps

from rest_framework import status
from rest_framework.response import Response


def check_ownership(func):
    """
    Make sure that user is able to edit only own sheets.
    """

    @wraps(func)
    def wrapper(view, request, *args, **kwargs):
        if kwargs["pk"] in request.user.sheets.values_list('id', flat=True):
            return func(view, request, *args, **kwargs)
        else:
            return Response(
                "Sheets can be modified only by sheet owner.",
                status=status.HTTP_403_FORBIDDEN,
            )

    return wrapper
