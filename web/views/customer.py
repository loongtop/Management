from crud import (CRUDSite,
                  model_handler_tuple, return_url, name_tuple,
                  HandlerList, Handler, RetrieveView, CreateView, DeleteView, DetailView, UpdateView,
                  func, StyleModelForm, Option,
                  mark_safe, pagination)


class CustomerConfig(RetrieveView):
    pass


handlerList = HandlerList(retrieve=CustomerConfig)
handler = handlerList.handler_dict
