from django.template import Library
from django.conf import settings
from rbac.utils import get_url
from collections import OrderedDict

register = Library()


@register.inclusion_tag('rbac/main_menu.html')
def main_menu(request):
    """
    create main menu
    :return:
    """
    menu_list = request.session[settings.MENU_SESSION_KEY]
    return {'menu_list': menu_list}


@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    """
    Create a secondary menu,
    :return:
    """
    ordered_dict = OrderedDict()
    menu_dict = request.session[settings.MENU_SESSION_KEY]
    ordered_dict.update({k: v for k, v in sorted(menu_dict.items(), key=lambda item: item[1])})

    # used to display the secondary menu
    for key, value in ordered_dict.items():
        value['class'] = 'hide'
        for child in value['children']:

            if child['id'] == request.current_selected_permission:
                child['class'] = 'active'
                child['class'] = ''
        ordered_dict[key] = value

    return {'menu_dict': ordered_dict}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    """
    :param request:
    :return:
    """
    return {'record_list': request.breadcrumb}


@register.filter
def has_permission(request, name):
    """
    :param request:
    :param name:
    :return:
    """
    return name in request.session[settings.PERMISSION_SESSION_KEY]


@register.simple_tag
def reverse_url(request, name, *args, **kwargs):
    """
    Generate a URL with the original search criteria (replaces the url in the template)
    :param request:
    :param name:
    :return:
    """
    return get_url.url_encode(request, name, *args, **kwargs)


def _help_get_menu_in_session(request):
    return request.session[settings.MENU_SESSION_KEY]
