from django.db.models import Model
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.urls import re_path

from .handler import Handler


class Create(Handler):
    """
    create an element
    """
    cls_name = 'create'
    create_template = None

    def create(self, request: WSGIRequest, *args, **kwargs):
        """
        create an element
        """
        modelform = self._get_modelform
        # GET request
        if request.method == 'GET':
            form = modelform()
            return render(request, self.create_template or 'crud/change.html', {'form': form})
        # POST request
        form = modelform(data=request.POST)
        if form.is_valid():
            response = Handler.save(form)
            return response or redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, self.create_template or 'crud/change.html', {'form': form})

    @property
    def _get_urls(self):
        return re_path(f'{self.cls_name}/$', self._wrapper(self.create), name=self._get_full_name(self.cls_name))
