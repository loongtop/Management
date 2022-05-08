from collections import OrderedDict, defaultdict
from django.shortcuts import render, redirect, HttpResponse
from django.forms import formset_factory
from django.conf import settings
from django.utils.module_loading import import_string

from rbac import models
from rbac.forms.permission import PermissionModelForm
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, MultiCreatePermissionForm, MultiUpdatePermissionForm
from rbac.utils import get_url


def menu_list(request):
    """
    List of menus and permissions
    :param request:
    :return:
    """
    # get main menu and sub menu
    menu_id = request.GET.get('mid')
    second_menus = []
    if models.Menu.objects.filter(id=menu_id).exists():
        second_menus = models.Permission.objects.filter(menu_id=menu_id)

    # get sub menu and permissions
    second_menu_id = request.GET.get('sid')
    permissions = []
    if models.Permission.objects.filter(id=second_menu_id).exists():
        permissions = models.Permission.objects.filter(parent_id=second_menu_id)

    # get all menu
    menu_all = models.Menu.objects.all()

    return render(request, 'rbac/menu_list.html', {'menus': menu_all,
                                                   'second_menus': second_menus,
                                                   'permissions': permissions,
                                                   'menu_id': menu_id,
                                                   'second_menu_id': second_menu_id,} )


def menu_create(request):
    """
    create a first level menu
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(get_url.url_params(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def menu_update(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    if not (obj := models.Menu.objects.filter(id=pk).first()):
        return HttpResponse('menu does not exist!')

    if request.method == 'GET':
        form = MenuModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(get_url.url_params(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def menu_del(request, pk):
    """

    :param request:
    :param pk:
    :return:
    """
    url = get_url.url_params(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Menu.objects.filter(id=pk).delete()
    return redirect(url)


def second_menu_create(request, menu_id):
    """
    create secondary menu
    :param request:
    :param menu_id: Selected primary menu ID (used to set default value)
    :return:
    """

    menu_object = models.Menu.objects.filter(id=menu_id).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_object})
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(get_url.url_params(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def second_menu_update(request, pk):
    """
    update secondary menu
    :param request:
    :param pk:
    :return:
    """

    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_object)
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(get_url.url_params(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def second_menu_del(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    url = get_url.url_encode(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)
