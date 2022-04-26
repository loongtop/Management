from django.urls import re_path
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

from .handler import Handler


class Delete(Handler):
    """Delete un element"""
    cls_name = 'delete'
    delete_template = None

    def delete(self, request: WSGIRequest, pk, *args, **kwargs):
        """Delete un element"""

        if delete_obj := self._get_objects(pk):
            HttpResponse('The data was already deleted!')

        current_url = self.reverse_list_url(*args, **kwargs)

        if request.method == 'GET':
            return render(request, self.delete_template or 'crud/delete.html', {'cancel': current_url})

        response = delete_obj.delete()
        return response or redirect(current_url)

    @property
    def _get_urls(self):
        url = fr'{self.cls_name}/(?P<pk>\d+)/$'
        return re_path(url, self._wrapper(self.delete), name=self._get_full_name(self.cls_name))
