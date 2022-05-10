"""Models for create the URLs"""
from django.urls import re_path

from crud import get_site, model_handler_tuple, name_tuple
from rbac.view import role, menu, permission
from rbac.models import Role, Menu, Permission

model_handlers = (model_handler_tuple(Role, role.handler),
                  model_handler_tuple(Menu, menu.handler),
                  model_handler_tuple(Permission, permission.handler),)


def urls(namespace, app_name="CRUD"):
    """
    generate the urls for web application to the project
    """
    site = get_site()
    site.set_name(name_tuple(namespace, app_name))
    site.register(model_handlers)
    return [re_path('', site.urls)]