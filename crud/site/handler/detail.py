from django.urls import re_path
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

from .handler import Handler
from .help import return_url


class DetailView(Handler):
    """show the detail of the selected element"""
    template_name = None

    def detail(self, request: WSGIRequest, pk, *args, **kwargs):
        """show the detail of the selected element"""

        if not (delete_obj := self._get_objects(pk).first()):
            message = 'The data does not exist, please re select!'
            return render(request, 'crud/wrong.html', {'message': message})

        current_url = self.reverse_list_url(*args, **kwargs)

        modelform = self._get_modelform
        if request.method == 'GET':
            form = modelform
            return render(request, self.template_name or 'crud/detail.html', {'form': form})

        return redirect(current_url)


    def set_url_tuple(self):
        url_name = f'{self.name}{self.url_name}'
        return return_url(url_name, self.detail, self.name)

