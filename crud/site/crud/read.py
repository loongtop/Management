"""read"""
from django.urls import re_path
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

from .handler import Handler
from crud.site.utils.pagination import Pagination

from collections import namedtuple
display_data = namedtuple('help', ('head', 'data', 'btn', 'pager'))


class Read(Handler):
    """
    read
    """
    cls_name = 'read'
    head_list = []
    order_list = []
    display_list = []
    per_page_count = 2
    has_create_btn = True

    def read(self, request: WSGIRequest):
        """
        read
        """

        # 1.get_order_list
        order = self.get_order_list
        objects = self._get_objects().order_by(*order)

        # 2. create button
        btn = self.get_create_btn

        # 3. pager
        count = objects.count()

        query_params = request.GET.copy()
        query_params._mutable = True

        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=count,
            base_url=request.path_info,
            query_params=query_params,
            per_page=self.per_page_count,
        )

        data_list = objects[pager.start: pager.end]

        # 4.head_list and data_list
        head, data = self.get_head_list, self.get_data_list(data_list)

        display = display_data(head, data, btn, pager)

        return render(request, 'crud/change_list.html', {'display': display})

    @property
    def get_display_list(self):
        lst = []
        lst.extend(self.display_list)
        if not lst:
            field0 = [self._get_meta().fields[0].name]
            lst.extend(field0)
        return lst

    @property
    def get_head_list(self):
        lst = []
        for name in self.get_display_list:
            verbose_name = self._get_meta().get_field(name).verbose_name
            yield verbose_name

    def get_data_list(self, data_list):
        for object in data_list:
            for head in self.get_display_list:
                yield getattr(object, head)

    @property
    def get_order_list(self):
        return self.order_list or ['-id', ]

    @property
    def get_create_btn(self):
        if self.has_create_btn:
            url = ''
            return f"<a class='btn btn-primary' href='{url}'>添加</a>"

    @property
    def _get_urls(self):
        return re_path(f'{self.cls_name}/$', self._wrapper(self.read), name=self._get_full_name(self.cls_name))




