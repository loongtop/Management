from .site import (CRUDSite,
                   Read, Create, Delete, Detail, Update,
                   model_handler_tuple, name_tuple)

from .site.utils.stylemodelform import StyleModelForm



def get_site():
    return CRUDSite()


def get_handler(read=Read, create=Create, delete=Delete, detail=Detail, update=Update):
    handler = {'read': read,  'create': create, 'delete': delete,
               'detail': detail, 'update': update}
    return handler
