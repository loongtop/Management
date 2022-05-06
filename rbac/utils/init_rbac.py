from django.conf import settings
from django.http import HttpResponse


def init_permission(request, current_user):
    """
    Initialization of user rights
    :param current_user: current user object
    :param request: request all relevant data
    :return:
    """
    request.session['user_info'] = {'id': current_user.id, 'nickname': current_user.nickname}

    # Permission information initialization
    # Obtain all permissions owned by this user based on the current user information and put them into the session.

    # All permissions of the current user

    permissions = current_user.role.filter(permission__isnull=False).values('permission__id',
                  'permission__title',
                  'permission__url',
                  'permission__alias',
                  'permission__parent_id',
                   'permission__parent_id__title',
                   'permission__parent_id__url',
                   'permission__parent_id__id',
                   'permission__menu__id',
                   'permission__menu__title',
                   'permission__menu__icon').distinct()

    # Initialization permission and menu information
    permission_dict, menu_dict = _help_init_permission(request, permissions)

    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict


def _help_init_permission(request, permissions):
    """_help_init_permission"""
    if not permissions:
        return HttpResponse('NO permissions in the database!')

    permission_dict, menu_dict = ({}, {})
    for item in permissions:
        pass

    return permission_dict, menu_dict




