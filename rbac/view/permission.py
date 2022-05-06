from django.shortcuts import render, redirect, HttpResponse

from rbac import models
from rbac.forms.permission import PermissionModelForm
from rbac.utils import get_url
# from .view_help import get_objects


def permission_create(request, second_menu_id):
    """
    permission_add
    :param request:
    :param second_menu_id:
    :return:
    """
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        if not (second_menu_object := models.Permission.objects.filter(id=second_menu_id).first()):
            return HttpResponse('The secondary menu does not exist, please select again!')
        form.instance.pid = second_menu_object
        form.save()
        return redirect(get_url.url_params(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def permission_update(request, pk):
    """
    permission_update
    :param request:
    :param pk:
    :return:
    """

    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_object)
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(get_url.url_params(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def permission_del(request, pk):
    """
    permission_del
    :param request:
    :param pk:
    :return:
    """

    url = get_url.url_params(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    obj = get_obj(models.Permission, pk)
    obj.delete()
    return redirect(url)