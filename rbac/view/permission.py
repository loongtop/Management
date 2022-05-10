from collections import OrderedDict

from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.module_loading import import_string
from django.http import HttpResponse

from crud import (return_url, HandlerList, Handler, RetrieveView, CreateView, DeleteView, DetailView, UpdateView,
                  func)

from rbac import models
from rbac.utils import get_url

from ._help_permission import (_help_get_permissions_dict, _help_get_menu_dict, _help_multi_permissions_update,
                               _help_multi_permissions_generate, _help_distribute_permissions_POST)

from rbac.forms.permission import PermissionModelForm


class Retrieve(RetrieveView):
    display_list = [func.detail, 'title', func.update_delete]
    template_name = 'rbac/role_list.html'


class Create(CreateView):
    template_name = 'rbac/change.html'
    sub_menu_id = 0

    def create(self, request, sub_menu_id):
        """
        #     permission_create
        #     :param request:
        #     :param second_menu_id:
        #     :return:
        """
        self.sub_menu_id = sub_menu_id

        if request.method == 'GET':
            form = PermissionModelForm()
            return render(request, 'rbac/change.html', {'form': form})

        form = PermissionModelForm(data=request.POST)
        if form.is_valid():
            if not (second_menu_object := models.Permission.objects.filter(id=sub_menu_id).first()):
                return HttpResponse('The secondary menu does not exist, please select again!')
            form.instance.parent_id = second_menu_object
            form.save()
            return redirect(get_url.url_params(request, 'rbac:menu_list'))

        return render(request, 'rbac/change.html', {'form': form})

    def set_url_tuple(self) -> return_url:
        url_name = f'{self.name}{self.url_name}'.replace('pk', 'sub_menu_id')
        return return_url(url_name, self.create, self.name)


class Delete(DeleteView):
    template_name = 'rbac/delete.html'


class Update(UpdateView):
    template_name = 'rbac/change.html'


class Detail(DetailView):
    template_name = 'rbac/change.html'


class Multi(Handler):
    def multi(self, request, *args, **kwargs):

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
                                                               'update_formset': update_formset, })

    def set_url_tuple(self) -> return_url:
        return return_url(self.name, self.multi, self.name)


class MultiDelete(Handler):
    def multi_delete(self, request, pk, *args, **kwargs):
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

    def set_url_tuple(self) -> return_url:
        url_name = f'{self.name}{self.url_name}'
        return return_url(url_name, self.multi_delete, self.name)


class Distribute(Handler):

    def distribute(self, request):
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

        all_menu_dict, all_second_menu_dict = _help_get_menu_dict(user_model_class, all_user_list, all_role_list,
                                                                  all_menu_list)

        # Get all roles owned by the current user
        user_has_roles = user_object.roles.all() if user_id else []
        user_has_roles_dict = {item.id: None for item in user_has_roles}

        return render(request, 'rbac/distribute_permissions.html', {'user_list': all_user_list,
                                                                    'role_list': all_role_list,
                                                                    'all_menu_list': all_menu_list,
                                                                    'user_id': user_id,
                                                                    'role_id': role_id,
                                                                    'user_has_roles_dict': user_has_roles_dict,
                                                                    'user_has_permissions_dict': user_has_permissions_dict, })

    def set_url_tuple(self) -> return_url:
        return return_url(self.name, self.distribute, self.name)


handlerList = HandlerList(retrieve=Retrieve, update=Update, create=Create, delete=Delete, detail=Detail)
handlerList.register(Multi, MultiDelete, Distribute)
handler = handlerList.handler_dict
