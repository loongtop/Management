from django.urls import re_path
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .handler import Handler


class Update(Handler):
    """
    update an element
    """
    cls_name = 'update'
    change_template = None

    def update(self, request: WSGIRequest, pk, *args, **kwargs):
        """
        update an element
        """
        if update_obj := self._get_objects(pk):
            return HttpResponse('The data does not exist, please re select!')

        modelform = self._get_modelform
        if request.method == "GET":
            form = modelform(instance=update_obj)
            return render(request, self.change_template or 'crud/change.html', {'form': form})

        form = modelform(data=request.POST, instance=update_obj)
        if form.is_valid():
            response = self.save(form)
            return response or redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, self.change_template or 'crud/change.html', {'form': form})

    @property
    def _get_urls(self):
        url = fr'{self.cls_name}/(?P<pk>\d+)/$'
        return re_path(url, self._wrapper(self.update), name=self._get_full_name(self.cls_name))
