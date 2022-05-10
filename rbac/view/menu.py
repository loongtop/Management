from django.shortcuts import render, redirect

from crud import (return_url, HandlerList, Handler, RetrieveView, CreateView, DeleteView, DetailView, UpdateView,
                  func)
from rbac import models
from rbac.forms.menu import SecondMenuModelForm
from rbac.utils import get_url


class Retrieve(RetrieveView):
    display_list = [func.detail, 'title', func.update_delete]

    # template_name = 'rbac/role_list.html'

    def retrieve(self, request, *args, **kwargs):
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
                                                       'second_menu_id': second_menu_id, })

    def set_url_tuple(self):
        url_name = self.name
        return return_url(url_name, self.retrieve, url_name)


class Create(CreateView):
    template_name = 'rbac/change.html'


class Delete(DeleteView):
    template_name = 'rbac/delete.html'


class Update(UpdateView):
    template_name = 'rbac/change.html'


class Detail(DetailView):
    template_name = 'rbac/change.html'


class SubCreate(Handler):
    menu_id = 0

    def sub_create(self, request, menu_id):
        """
        #     create secondary menu
        #     :param request:
        #     :param menu_id: Selected primary menu ID (used to set default value)
        #     :return:
        #     """
        #
        self.menu_id = menu_id
        menu_object = models.Menu.objects.filter(id=menu_id).first()

        if request.method == 'GET':
            form = SecondMenuModelForm(initial={'menu': menu_object})
            return render(request, 'rbac/change.html', {'form': form})

        form = SecondMenuModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(get_url.url_params(request, 'rbac:menu_list'))

        return render(request, 'rbac/change.html', {'form': form})

    def set_url_tuple(self) -> return_url:
        url_name = f'{self.name}{self.url_name}'.replace('pk', 'menu_id')
        return return_url(url_name, self.sub_create, self.name)


class SubUpdate(Handler):
    def sub_update(request, pk):
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

    def set_url_tuple(self) -> return_url:
        url_name = f'{self.name}{self.url_name}'
        return return_url(url_name, self.sub_update, self.name)


class SubDelete(Handler):
    def sub_delete(request, pk):
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

    def set_url_tuple(self) -> return_url:
        url_name = f'{self.name}{self.url_name}'
        return return_url(url_name, self.sub_delete, self.name)


handlerList = HandlerList(retrieve=Retrieve, update=Update, create=Create, delete=Delete, detail=Detail)
handlerList.register(SubCreate, SubUpdate, SubDelete)
handler = handlerList.handler_dict
