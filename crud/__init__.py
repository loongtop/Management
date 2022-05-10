from .site import (CRUDSite,
                   model_handler_tuple, return_url, name_tuple,
                   HandlerList, Handler, RetrieveView, CreateView, DeleteView, DetailView, UpdateView,
                   func, StyleModelForm, Option,
                   mark_safe, pagination)


def get_site():
    return CRUDSite()



