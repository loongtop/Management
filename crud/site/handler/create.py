from django.db.models import Model
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from .handler import Handler
from .help import return_url


class CreateView(Handler):
    """
    create an element
    """
    template_name = None

    def create(self, request: WSGIRequest, *args, **kwargs):
        """
        create an element
        """
        modelform = self._get_modelform
        # GET request
        if request.method == 'GET':
            form = modelform()
            return render(request, self.template_name or 'crud/change.html', {'form': form})
        # POST request
        form = modelform(data=request.POST)
        if form.is_valid():
            response = Handler.save(form)
            return response or redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, self.template_name or 'crud/change.html', {'form': form})


    def set_url_tuple(self):
        url_name = self.name
        return return_url(url_name, self.create, url_name)