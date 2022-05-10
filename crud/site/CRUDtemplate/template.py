from crud import (CRUDSite,
                  model_handler_tuple, return_url, name_tuple,
                  HandlerList, Handler, RetrieveView, CreateView, DeleteView, DetailView, UpdateView,
                  func, StyleModelForm, Option,
                  mark_safe, pagination)


class Retrieve(RetrieveView):
    display_list = [func.detail, 'title', func.update_delete]
    template_name = '/rbac/role_list.html'


class Create(CreateView):
    template_name = '/rbac/change.html'


class Delete(DeleteView):
    template_name = '/rbac/delete.html'


class Update(UpdateView):
    template_name = '/rbac/change.html'


class Detail(DetailView):
    template_name = '/rbac/change.html'



handlerList = HandlerList(retrieve=Retrieve)
handler = handlerList.handler_dict


