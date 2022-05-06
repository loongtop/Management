from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

from rbac import models
from rbac.forms.role import RoleModelForm


def role_list(request):
    """
    role_list
    :param request:
    :return:
    """
    role_queryset = models.Role.objects.all()

    return render(request, 'rbac/role_list.html', {'roles': role_queryset})


def role_create(request):
    """
    role_add
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = RoleModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = RoleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))

    return render(request, 'rbac/change.html', {'form': form})


def role_update(request, pk):
    """
    role_edit
    :param request:
    :param pk: 要修改的角色ID
    :return:
    """
    obj = models.Role.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('the role does not exist!')
    if request.method == 'GET':
        form = RoleModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = RoleModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))

    return render(request, 'rbac/change.html', {'form': form})


def role_del(request, pk):
    """
    role_del
    :param request:
    :param pk:
    :return:
    """
    origin_url = reverse('rbac:role_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})

    models.Role.objects.filter(id=pk).delete()
    return redirect(origin_url)