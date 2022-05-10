from crud import (CRUDSite,
                  model_handler_tuple, return_url, name_tuple,
                  HandlerList, Handler, RetrieveView, CreateView, DeleteView, DetailView, UpdateView,
                  func, StyleModelForm, Option,
                  mark_safe, pagination)


class CourseHandlerCFG(RetrieveView):
    display_list = [func.detail, 'name']
    # pass


handlerList = HandlerList(retrieve=CourseHandlerCFG)
handler = handlerList.handler_dict