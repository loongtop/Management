from crud import (CRUDSite,
                  model_handler_tuple, return_url, name_tuple,
                  HandlerList, Handler, RetrieveView, CreateView, DeleteView, DetailView, UpdateView,
                  func, StyleModelForm, Option,
                  mark_safe, pagination)


class DepartmentCFG(RetrieveView):
    display_list = [func.detail, 'title', func.update_delete]


handlerList = HandlerList(retrieve=DepartmentCFG)
handler = handlerList.handler_dict