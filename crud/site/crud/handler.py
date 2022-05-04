"""The base class for deriving """
import functools
import itertools

from django.db.models import Model
from django.urls import reverse
from django.shortcuts import render, redirect

from .help.namedtuple import name_tuple
from .help.stylemodelform import StyleModelForm


class Handler(object):
    """The base class for deriving """
    cls_name = {'create': 'create', 'retrieve': 'retrieve', 'update': 'update',
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
        """retrieve the object in the database according to the PK key value"""
        objects = self._model.objects
        if not pk:
            return objects.all()
        return objects.filter(pk=pk)

    def reverse_list_url(self, *args, **kwargs):
        """generate a return address for the operation """
        reverse_name = self.get_reverse_name('retrieve')
        base_url = reverse(reverse_name, args=args, kwargs=kwargs)

        if param := self.request.GET.get('_filter'):
            return f'{base_url}?{param}'
        return base_url

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

    def get_reverse_name(self, operation_name):
        """
        This methods is used for get_reverse_name
        """
        return f'{self.name.namespace}:{self._get_full_name(operation_name)}'

    def is_obj_exists(self, pk, message='The data does not exist, please re select!'):
        if not (obj := self._get_objects(pk).first()):
            return render(self.request, 'crud/wrong.html', {'message': message})
        return obj

    @property
    def _get_urls(self):
        """
        you must Implement this method!
        """
        raise NotImplementedError('you must Implement this method!')

    @property
    def extra_urls(self):
        return []

    @property
    def urls(self):
        """
        the interface that give urls
        """
        lst = [self._get_urls]
        lst.extend(self.extra_urls)
        return lst
