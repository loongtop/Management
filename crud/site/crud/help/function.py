from collections import namedtuple

from django.db.models import Model
from django.http import QueryDict
from django.urls import reverse

from crud.site.utils.mark_safe import mark_safe


def reverse_url(param, handler=None, *args, **kwargs):
    """
    :param handler:
    :param param:
    :return:
    """
    reverse_name = handler.get_reverse_name(param)
    base_url = reverse(reverse_name, args=args, kwargs=kwargs)

    add_url = base_url
    if handler.request.GET:
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
    return mark_safe('<input type="checkbox" name="pk" value="replace" />', obj.pk)


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
    return mark_safe('<a href="replace">Update</a>', url)


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
    return mark_safe('<a href="replace">Delete</a>', url)


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
    return mark_safe('<a href="replace">name</a>', url)


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

    tpl_update = mark_safe('<a href="replace"> Update </a>', url_update)
    tpl_delete = mark_safe('<a href="replace"> Delete </a>', url_delete)
    return mark_safe(tpl_update + '||' + tpl_delete, '')


def create(handler=None, obj: Model = None, *args, **kwargs):
    """
    :param handler:
    :param obj:
    :return:
    """
    if handler.has_create_btn:
        create_url = reverse_url('create', handler, *args, **kwargs)
        return mark_safe('<a class="btn btn-primary" href="replace">Create</a>', create_url)


def reset_pwd(self, obj=None, is_header=None, *args, **kwargs):
    if is_header:
        return 'Reset password'
    reset_url = reverse_url('reset_pwd', pk=obj.pk)
    return mark_safe("<a href='replace'>Reset password</a>", reset_url)


def create_function():
    """create_function """
    function = namedtuple('function', 'checkbox, update, delete, detail, update_delete, create, reset_pwd')
    return function(checkbox, update, delete, detail, update_delete, create, reset_pwd)


func = create_function()
