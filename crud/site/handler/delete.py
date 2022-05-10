from django.urls import re_path
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

from .handler import Handler
from .help import return_url


class DeleteView(Handler):
    """Delete un element"""
    template_name = None

    def delete(self, request: WSGIRequest, pk, *args, **kwargs):
        """Delete un element"""

        if not (delete_obj := self._get_objects(pk).first()):
            message = 'The data was already deleted!'
            return render(request, 'crud/wrong.html', {'message': message})

        current_url = self.reverse_list_url(*args, **kwargs)

        if request.method == 'GET':
            return render(request, self.template_name or 'crud/delete.html', {'cancel': current_url})

        # response = delete_obj.delete()
        delete_obj.delete()
        return redirect(current_url)


    def set_url_tuple(self):
        url_name = f'{self.name}{self.url_name}'
        return return_url(url_name, self.delete, self.name)
