from django.template import Library
from django.conf import settings
from rbac.utils import get_url
from collections import defaultdict

register = Library()


@register.inclusion_tag('rbac/main_menu.html')
def main_menu(request):
    """
    create main menu
    :return:
    """
    menu_list = request.session[settings.MENU_SESSION_KEY]
    return {'menu_list': menu_list}


@register.filter
def has_permission(request, name):
    """
    :param request:
    :param name:
    :return:
    """
    session_dict = defaultdict(str)
    session_dict.update(request.session[settings.PERMISSION_SESSION_KEY])

    return session_dict.get(name)


@register.simple_tag
def reverse_url(request, name, *args, **kwargs):
    """
    Generate a URL with the original search criteria (replaces the url in the template)
    :param request:
    :param name:
    :return:
    """
    return get_url.url_params(request, name, *args, **kwargs)