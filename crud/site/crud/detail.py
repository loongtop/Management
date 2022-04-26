from django.urls import re_path
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

from .handler import Handler


class Detail(Handler):
    """show the detail of the selected element"""
    cls_name = 'detail'

    def detail(self, request: WSGIRequest, pk, *args, **kwargs):
        """show the detail of the selected element"""
        if detail_obj := self._get_objects(pk=pk):
            return HttpResponse('The data does not exist, please re select!')

        current_url = self.reverse_list_url(*args, **kwargs)

        modelform = self._get_modelform
        if request.method == 'GET':
            form = modelform(instance=detail_obj)
            return render(request, 'crud/detail.html', {'form': form})

        return redirect(current_url)

    @property
    def _get_urls(self):
        url = fr'{self.cls_name}/(?P<pk>\d+)/$'
        return re_path(url, self._wrapper(self.detail), name=self._get_full_name(self.cls_name))
