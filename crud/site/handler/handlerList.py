from .create import CreateView
from .delete import DeleteView
from .detail import DetailView
from .retrieve import RetrieveView
from .update import UpdateView


class HandlerList(object):
    """HandlerList"""

    def __init__(self, retrieve=RetrieveView, create=CreateView, delete=DeleteView, detail=DetailView, update=UpdateView):
        self._handler_dict = {'retrieve': retrieve,
                              'create': create,
                              'delete': delete,
                              'detail': detail,
                              'update': update}

    @property
    def handler_dict(self):
        return self._handler_dict

    def register(self, *handlerlist):
        handler_dict = {}

        for handler in handlerlist:
            name = str.lower(handler.__name__)
            if name in self.handler_dict.keys():
                raise BaseException(f'key 重复')
            handler_dict[name] = handler

        self._handler_dict.update(handler_dict)
