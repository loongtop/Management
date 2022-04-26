"""read"""
from django.urls import re_path
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

from .handler import Handler


class Read(Handler):
    """
    read
    """
    cls_name = 'read'

    def read(self, request: WSGIRequest):
        """
        read
        """

        data_list = self._get_objects()
        return render(request, 'crud/change_list.html', {'data_list': data_list})

    @property
    def _get_urls(self):
        return re_path(f'{self.cls_name}/$', self._wrapper(self.read), name=self._get_full_name(self.cls_name))
