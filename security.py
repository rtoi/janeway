from functools import wraps

from django.shortcuts import reverse, redirect, get_object_or_404, Http404
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from plugins.typesetting import models
from security.decorators import base_check, deny_access
from submission import models as submission_models
from core import models as core_models


def proofreader_for_article_required(func):
    """
    Checks that the current user is the proofreader for the current task.
    :param func: the function to callback from the decorator
    :return: either the function call or raises an PermissionDenied
    """

    def wrapper(request, *args, **kwargs):
        if not base_check(request):
            return redirect(
                '{0}?next={1}'.format(
                    reverse('core_login'),
                    request.path_info
                )
            )

        elif request.user.is_editor(request) or request.user.is_staff or request.user.is_production(request):
            return func(request, *args, **kwargs)

        # User is Assigned as proofreader, regardless of role
        elif models.GalleyProofing.objects.filter(
                pk=kwargs['assignment_id'],
                proofreader=request.user,
                cancelled=False,
                completed__isnull=True,
                round__article__journal=request.journal
        ).exists():
            return func(request, *args, **kwargs)

        else:
            deny_access(request)

    return wrapper


def require_not_notified(object_model):
    """
    Decorator that checks if an object's notified boolean attribute is True
    and redirects
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            assignment_id = kwargs.get('assignment_id')

            if not assignment_id:
                raise Http404

            object_to_check = get_object_or_404(
                object_model,
                pk=assignment_id,
            )

            if object_to_check.notified:
                raise PermissionDenied("Notification for this assignment has already been sent.")

            return func(request, *args, **kwargs)
        return inner
    return decorator


def user_can_manage_file(func):
    """
    A decorator for checking if the current user can manage a file.
    """
    def wrapper(request, *args, **kwargs):
        file_object_id = kwargs.get('file_id', None)

        if not file_object_id:
            raise Http404

        file_object = get_object_or_404(
            core_models.File,
            pk=file_object_id,
        )

        if can_manage_file(request, request.user, file_object):
            return func(request, *args, **kwargs)

        return deny_access(request)

    return wrapper



def can_manage_file(request, user, file_object):
    """
    Determines if a user can view and download a file in the Typesetting Plugin.
    """
    if request.user.is_anonymous():
        return False

    if (
        request.user.is_staff or 
        request.user.is_editor(request) or
        request.user.is_production(request) or 
        file_object.owner == request.user
    ):
        return True

    # deny access to all others
    return False
