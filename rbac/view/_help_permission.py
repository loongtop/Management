
from collections import defaultdict

from django.conf import settings
from django.forms import formset_factory
from django.shortcuts import render, redirect, HttpResponse
from django.utils.module_loading import import_string

from rbac import models
from rbac.forms.permission import MultiCreatePermissionForm, MultiUpdatePermissionForm


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
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values('id',
                                                                                              'permissions').distinct()
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