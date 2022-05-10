from django.urls import re_path
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .handler import Handler
from .help import return_url


class UpdateView(Handler):
    """
    update an element
    """
    template_name = None

    def update(self, request: WSGIRequest, pk, *args, **kwargs):
        """
        update an element
        """
        if not (update_obj := self._get_objects(pk).first()):
            message = 'The data does not exist, please re select!'
            return render(request, 'crud/wrong.html', {'message': message})

        modelform = self._get_modelform
        if request.method == "GET":
            form = modelform(instance=update_obj)
            return render(request, self.template_name or 'crud/change.html', {'form': form})

        form = modelform(data=request.POST, instance=update_obj)
        if form.is_valid():
            response = self.save(form)
            return response or redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, self.change_template or 'crud/change.html', {'form': form})


    def set_url_tuple(self):
        url_name = f'{self.name}{self.url_name}'
        return return_url(url_name, self.update, self.name)
