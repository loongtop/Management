from crud import (CRUDSite,
                  model_handler_tuple, return_url, name_tuple,
                  HandlerList, Handler, RetrieveView, CreateView, DeleteView, DetailView, UpdateView,
                  func, StyleModelForm, Option,
                  mark_safe, pagination)

class SchoolConfig(RetrieveView):
    display_list = [func.detail, 'title', func.update_delete]
    # pass


handlerList = HandlerList(retrieve=SchoolConfig)
handler = handlerList.handler_dict

