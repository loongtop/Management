from collections import namedtuple

from django.db.models import Model
from django.http import QueryDict
from django.utils.safestring import mark_safe
from django.urls import reverse


def reverse_url(param, handler=None, *args, **kwargs):
    """
    :param handler:
    :param param:
    :return:
    """
    reverse_name = handler.get_reverse_name(param)
    base_url = reverse(reverse_name, args=args, kwargs=kwargs)
    if not handler.request.GET:
        add_url = base_url
    else:
        param = handler.request.GET.urlencode()
        new_query_dict = QueryDict(mutable=True)
        new_query_dict['_filter'] = param
        url_encode = new_query_dict.urlencode()
        add_url = f"{base_url}?{url_encode}"
    return add_url


def checkbox(handler=None, obj: Model = None, is_header=None):
    """
    :param handler:
    :param obj:
    :param is_header:
    :return:
    """
    if is_header:
        return "Operation"
    return mark_safe(f'<input type="checkbox" name="pk" value="{obj.pk}" />')


def update(handler=None, obj: Model = None, is_header=None):
    """
    :param handler:
    :param obj:
    :param is_header:
    :return:
    """
    if is_header:
        return "Update"

    url = reverse_url('update', handler, pk=obj.pk)
    return mark_safe(f'<a href="{url}">Update</a>')


def delete(handler=None, obj: Model = None, is_header=None):
    """
    :param handler:
    :param obj:
    :param is_header:
    :return:
    """
    if is_header:
        return "Delete"
    url = reverse_url('delete', handler, pk=obj.pk)
    return mark_safe(f'<a href="{url}">Delete</a>')


def detail(handler=None, obj: Model = None, is_header=None):
    """
    :param handler:
    :param obj:
    :param is_header:
    :return:
    """
    if is_header:
        return "Detail"
    url = reverse_url('detail', handler, pk=obj.pk)
    return mark_safe(f'<a href="{url}">replace_place</a>')


def update_delete(handler=None, obj: Model = None, is_header=None):
    """
    :param handler:
    :param obj:
    :param is_header:
    :return:
    """
    if is_header:
        return 'Operation'
    url_update = reverse_url('update', handler, pk=obj.pk)
    url_delete = reverse_url('delete', handler, pk=obj.pk)

    tpl = f'<a href="{url_update}"> Update </a>| |<a href="{url_delete}"> Delete </a>'
    return mark_safe(tpl)


def create(handler=None, obj: Model = None, *args, **kwargs):
    """
    :param handler:
    :param obj:
    :return:
    """
    if handler.has_create_btn:
        create_url = reverse_url('create', handler, *args, **kwargs)
        return f'<a class="btn btn-primary" href="{create_url}">Create</a>'


def create_function():
    """create_function """
    function = namedtuple('function', 'checkbox, update, delete, detail, update_delete, create')
    return function(checkbox, update, delete, detail, update_delete, create)


fun = create_function()
