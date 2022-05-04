from .site import (CRUDSite,
                   Retrieve, Create, Delete, Detail, Update,
                   model_handler_tuple, name_tuple,
                   )
from .site.crud.help.function import func

from crud.site.crud.help.stylemodelform import StyleModelForm


def get_site():
    return CRUDSite()


def get_handler(retrieve=Retrieve, create=Create, delete=Delete, detail=Detail, update=Update):
    handler = {'retrieve': retrieve, 'create': create, 'delete': delete,
               'detail': detail, 'update': update}
    return handler
