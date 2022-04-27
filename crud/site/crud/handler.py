"""The base class for deriving """
from django.db.models import Model
import functools

from crud.site.utils import name_tuple
from crud.site.utils.stylemodelform import StyleModelForm


class Handler(object):
    """The base class for deriving """
    cls_name = {'create': 'create', 'read': 'read', 'update': 'update',
                'delete': 'delete', 'detail': 'detail'}

    def __init__(self, model: Model, name: name_tuple, prev=None):
        self.name = name
        self._model = model
        self._prev = prev
        self.request = None

        self.modelform = None

    @classmethod
    def save(cls, form):
        """
        Hook method that reserved before saving data with ModelForm
        :param form:
        :return:
        """
        form.save()

    def _get_objects(self, pk=None):
        objects = self._model.objects
        if not pk:
            return objects.all()
        return objects.filter(pk=pk)

    def reverse_list_url(self, *args, **kwargs):
        pass

    @property
    def _get_modelform(self):
        if self.modelform:
            return self.modelform

        class DefaultModelform(StyleModelForm):
            class Meta:
                model = self._model
                fields = '__all__'

        return DefaultModelform

    def _get_meta(self, model: Model = None):
        """get meta data"""
        meta = self._model._meta
        if model:
            meta = model._meta
        return meta

    def _wrapper(self, function):
        @functools.wraps(function)
        def inner(request, *args, **kwargs):
            self.request = request
            return function(self.request, *args, **kwargs)
        return inner

    def _get_full_name(self, operation_name):
        """
        this methods is used to get_app_model_name
        """
        app_label = self._get_meta(self._model).app_label
        model_name = self._get_meta(self._model).model_name

        if self._prev:
            return f'{app_label}_{model_name}_{self._prev}_{operation_name}'
        return f'{app_label}_{model_name}_{operation_name}'

    def _get_reverse_name(self, operation_name):
        """
        This methods is used for get_reverse_name
        """
        return f'{self.name.namespace}:{self._get_full_name(operation_name)}'

    @property
    def _get_urls(self):
        """
        you must Implement this method!
        """
        raise NotImplementedError('you must Implement this method!')

    @property
    def urls(self):
        """
        the interface that give urls
        """
        return self._get_urls
