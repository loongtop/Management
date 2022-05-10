"""Model for create Urls"""
import itertools
from django.urls import re_path

from .handler import Handler, name_tuple


class Site(object):
    """
     class for deriving class for CRUD
    """

    def __init__(self, name: name_tuple):
        self.name = name

    def set_name(self, name: name_tuple):
        """
         the interface ot give a name to the site!
        """
        self.name = name

    def urls(self):
        """
         You must implement this method!
        """
        raise NotImplementedError('You must implement this method!')

    def _get_urls(self):
        """
         You must implement this method!
        """
        raise NotImplementedError('You must implement this method!')


class CRUDSite(Site):
    """
    class for create operation CURD and Urls
    """

    def __init__(self, name: name_tuple = name_tuple('CRUD', 'CRUD')):
        super(CRUDSite, self).__init__(name)

        self._registry = []

    def register(self, model_handlers, pre: str = None):
        """
        args : the set of model and handler
        prev : adding a prefix to urls
        return:
        """
        for model_handler in model_handlers:
            self._registry.append({'model': model_handler[0],
                                   'handler': model_handler[1],
                                   'pre': pre})

    def _create_urls(self, model, handler, pre=None):
        """
        the real function that create urls
        """
        urlpatterns = []

        for operation in handler.values():
            operator: Handler = operation(model, self.name, pre)
            urlpatterns.extend(operator.urls)

        return urlpatterns

    @property
    def _get_urls(self):
        """
        """
        urlpatterns = []
        for model_handler_pre in self._registry:
            model = model_handler_pre.get('model')
            handler = model_handler_pre.get('handler')

            url = f'{model._meta.app_label}/{model._meta.model_name}/'

            if pre := model_handler_pre.get('pre'):
                urlpatterns.append(re_path(fr'^{url}/{pre}',
                                           (self._create_urls(model, handler, pre), None, None)))
            else:
                urlpatterns.append(re_path(fr'^{url}',
                                           (self._create_urls(model, handler), None, None)))

        return urlpatterns

    @property
    def urls(self):
        """
        the interface that give urls
        """
        return self._get_urls, self.name.app_name, self.name.namespace
