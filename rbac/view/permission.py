from collections import OrderedDict
from django.shortcuts import render, redirect, HttpResponse
from django.utils.module_loading import import_string
from django.conf import settings
from django.forms import formset_factory

from rbac import models
from rbac.forms.permission import PermissionModelForm
from rbac.utils import get_url


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
        form.instance.parent_id = second_menu_object
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

    models.Permission.objects.filter(pk=pk).delete()
    return redirect(url)


def multi_permissions(request):
    """
    Bulk Action Permissions
    :param request:
    :return:
    """
    generate_formset, generate_formset_class = _help_multi_permissions_generate(request)
    update_formset, update_formset_class = _help_multi_permissions_update(request)

    # get all url in the project
    all_url_dict = get_url.get_all_url()
    router_name_set = set(all_url_dict.keys())

    # Get all the URLs in the database
    permission_dict = OrderedDict()
    permissions = models.Permission.objects.all().values('id', 'title', 'alias', 'url', 'menu_id', 'parent_id_id')
    permission_name_set = set()

    for row in permissions:
        permission_dict.update({row['alias']: row})
        permission_name_set.add(row['alias'])

    for name, value in permission_dict.items():
        router_row_dict = all_url_dict.get(name)  # {'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = 'inconsistency between routing and database!'

    # What permissions should be added, deleted, and modified?
    #  Calculate the name that should be added
    if not generate_formset:
        generate_name_list = router_name_set.difference(permission_name_set)
        generate_formset = generate_formset_class(
            initial=[row_dict for name, row_dict in all_url_dict.items() if name in generate_name_list])

    # Calculate the name that should be deleted
    delete_name_list = permission_name_set.difference(router_name_set)
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # Calculate the name that should be updated
    if not update_formset:
        update_name_list = permission_name_set.union(router_name_set)
        update_formset = update_formset_class(
            initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list])

    return render(request, 'rbac/multi_permissions.html', {'generate_formset': generate_formset,
                                                           'delete_row_list': delete_row_list,
                                                           'update_formset': update_formset,})


def multi_permissions_del(request, pk):
    """
    Permission removal for bulk pages
    :param request:
    :param pk:
    :return:
    """
    url = get_url.url_encode(request, 'rbac:multi_permissions')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


###################
def _help_get_menu_dict(user_model_class, all_menu_list):

    all_menu_dict = defaultdict(None)
    for item in all_menu_list:
        item['children'] = []
        all_menu_dict.update({item['id']: item})

    # All secondary menus
    all_second_menu_list = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')
    all_second_menu_dict = defaultdict(None)
    for row in all_second_menu_list:
        row['children'] = []
        all_second_menu_dict.update({row['id']: row})

        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)

    # All three-level menus (cannot do menu permissions)
    all_permission_list = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'parent_id_id')

    for row in all_permission_list:
        pid = row['parent_id_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(row)

    return all_menu_dict, all_second_menu_dict


def _help_get_permissions_dict(role_object, user_object):
    # Get all permissions of the current user user user
    # If the selected role is selected, the privileges of the selected role will be displayed first
    # If no role is selected, only display the permissions the user has
    user_has_permissions_dict = defaultdict(None)

    if role_object:
        user_has_permissions = role_object.permissions.all()
        user_has_permissions_dict = {item.id: None for item in user_has_permissions}
    elif user_object:
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values('id', 'permissions').distinct()
        user_has_permissions_dict = {item['permissions']: None for item in user_has_permissions}
    else:
        user_has_permissions_dict = {}

    return user_has_permissions_dict


def _help_distribute_permissions_POST(request, user_id, user_model_class):
    """_help_distribute_permissions"""
    if user_object := user_model_class.objects.filter(id=user_id).first():
        role_id = request.GET.get('rid')

    if not (role_object := models.Role.objects.filter(id=role_id).first()):
        role_id = None

    if request.method == 'POST' and request.POST.get('type') == 'role':
        role_id_list = request.POST.getlist('roles')
        # User and role relationships are added to the third table (relationship table)
        if not user_object:
            return HttpResponse('Please select a user before assigning a role!')
        user_object.roles.set(role_id_list)

    if request.method == 'POST' and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_object:
            return HttpResponse('Please select a role before assigning permissions!')
        role_object.permissions.set(permission_id_list)

    return role_id, user_object, role_object


def _help_multi_permissions_generate(request):
    """Help function"""
    generate_formset = None
    generate_formset_class = formset_factory(MultiCreatePermissionForm, extra=0)

    if request.method == 'POST' and 'generate' == request.GET.get('type'):
        # pass # 批量添加
        formset = generate_formset_class(data=request.POST)
        if formset.is_valid():
            object_list = []
            post_row_list = formset.cleaned_data
            has_error = False
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_object = models.Permission(**row_dict)
                    new_object.validate_unique()
                    object_list.append(new_object)
                except Exception as e:
                    formset.errors[i].update(e)
                    generate_formset = formset
                    has_error = True
            if not has_error:
                models.Permission.objects.bulk_create(object_list, batch_size=100)
        else:
            generate_formset = formset

    return generate_formset, generate_formset_class


def _help_multi_permissions_update(request):
    """Help function"""
    update_formset = None
    update_formset_class = formset_factory(MultiUpdatePermissionForm, extra=0)

    if request.method == 'POST' and 'update' == request.GET.get('type'):
        # pass  # 批量更新
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    row_object = models.Permission.objects.filter(id=permission_id).first()
                    for k, v in row_dict.items():
                        setattr(row_object, k, v)
                    row_object.validate_unique()
                    row_object.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset
        else:
            update_formset = formset

    return update_formset, update_formset_class


def distribute_permissions(request):
    """
    distribute_permissions
    :param request:
    :return:
    """
    user_id = request.GET.get('uid')
    user_model_class = import_string(settings.RBAC_USER_MODEL_CLASS)

    # User table in business
    role_id, user_object, role_object = _help_distribute_permissions_POST(request, user_id, user_model_class)

    user_has_permissions_dict = _help_get_permissions_dict(role_object, user_object)

    # get list of user, role and menu
    all_user_list = user_model_class.objects.all()
    all_role_list = models.Role.objects.all()
    all_menu_list = models.Menu.objects.values('id', 'title')

    all_menu_dict, all_second_menu_dict = _help_get_menu_dict(user_model_class, all_user_list, all_role_list, all_menu_list)

    # Get all roles owned by the current user
    user_has_roles = user_object.roles.all() if user_id else []
    user_has_roles_dict = {item.id: None for item in user_has_roles}

    return render(request, 'rbac/distribute_permissions.html', {'user_list': all_user_list,
                                                                'role_list': all_role_list,
                                                                'all_menu_list': all_menu_list,
                                                                'user_id': user_id,
                                                                'role_id': role_id,
                                                                'user_has_roles_dict': user_has_roles_dict,
                                                                'user_has_permissions_dict': user_has_permissions_dict,})
