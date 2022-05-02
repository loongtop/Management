"""read"""
import itertools
from collections import defaultdict
from types import FunctionType
from django.urls import re_path
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import mark_safe
from django.db.models import Q

from .handler import Handler
from crud.site.utils.pagination import Pagination
from crud.site.crud.help.function import fun

from collections import namedtuple
display = namedtuple('help', 'head, data, btn, pager, search_list, search_value, action_dict, search_group_row_list')


class Read(Handler):
    """
    read
    """
    cls_name = 'read'
    head_list = []
    order_list = []
    display_list = []
    action_list = []
    search_list = []
    search_group = []
    per_page_count = 10
    has_create_btn = True

    def read(self, request: WSGIRequest, *args, **kwargs):
        """
        read view
        """

        # handle action
        action_dict = defaultdict(None)
        if request.method == 'POST':
            action_dict.update({func.__name__: func.text for func in self.get_action_list})

            action_name = request.POST.get('action')
            b_action_name = action_dict.get(action_name)

            if all(list[action_name, b_action_name]):
                return getattr(self, action_name)(request, *args, **kwargs)

        # search list
        conn = Q(_connector='OR')
        search_list = self.search_list
        if search_value := request.GET.get('q', ''):
            for item in search_list:
                conn.children.append((item, search_value))

        # order list
        order = self.get_order_list
        search_group_condition = self.get_search_group_condition(request)
        objs = self._get_objects().filter(conn).filter(**search_group_condition).order_by(*order)

        # create button
        btn = fun.create(self, *args, **kwargs)

        # pager
        count = objs.count()

        query_params = request.GET.copy()
        query_params._mutable = True

        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=count,
            base_url=request.path_info,
            query_params=query_params,
            per_page=self.per_page_count,
        )

        objects_pager = objs[pager.start: pager.end]

        # head_list and data_list
        head, data = self.get_head_list, self.get_data_list(objects_pager)

        # combined search
        search_group_row_list = []
        # ['gender', 'depart' or .....]
        search_group = self.get_search_group
        for option_object in search_group:
            row = option_object.get_queryset_or_tuple(self.model_class, request, *args, **kwargs)
            search_group_row_list.append(row)

        display_front = display(head, data, btn, pager, search_list, search_value, action_dict, search_group_row_list)

        return render(request, 'crud/change_list.html', {'display': display_front})

    @property
    def get_display_list(self):
        """get display list"""
        lst = []
        if not self.display_list:
            field0 = [self._get_meta().fields[0].name]
            return itertools.chain(lst, field0)
        return itertools.chain(lst, self.display_list)

    @property
    def get_head_list(self):
        """get head list"""
        for name_fun in self.get_display_list:
            if not isinstance(name_fun, FunctionType):
                verbose_name = self._get_meta().get_field(name_fun).verbose_name
            else:
                if name_fun.__name__ == 'detail':
                    continue
                verbose_name = name_fun(is_header=True)
            yield verbose_name

    def get_data_list(self, objects_pager):
        """get data list"""
        detail_link_str = defaultdict(str)

        for obj in objects_pager:
            lst = []
            for name_fun in self.get_display_list:
                if not isinstance(name_fun, FunctionType):
                    data = getattr(obj, name_fun)
                else:
                    data = name_fun(handler=self, obj=obj, is_header=False)

                    # get the detail str of href="../../detail/?" for the column name of title
                    if name_fun.__name__ == 'detail':
                        detail_link_str['is_detail'] = data
                        continue

                # make the data(name of title) which next to detail a hyperlink
                if link_str := detail_link_str.get('is_detail'):
                    data = mark_safe(link_str.replace('replace_place', data))
                    detail_link_str.clear()

                lst.append(data)
            yield lst

    @property
    def get_order_list(self):
        """get order list"""
        return self.order_list or ['-id', ]

    @property
    def get_action_list(self):
        """get action list"""
        return self.action_list

    def action_multi_delete(self, request, *args, **kwargs):
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()

    action_multi_delete.text = "Batch Deletion"

    @property
    def get_search_list(self):
        """get action list"""
        return self.search_list

    @property
    def get_search_group(self):
        return self.search_group

    def get_search_group_condition(self, request):
        """
        Get parameters for combinatorial searchGet parameters for combinatorial search
        :param request:
        :return:
        """
        condition = defaultdict(None)
        # ?depart=1&gender=2&page=123&q=999
        for option in self.get_search_group:
            if option.is_multi:
                # tags=[1,2]
                if not (values_list := request.GET.getlist(option.field)):
                    continue
                condition[f'{option.field}__in'] = values_list
            else:
                if not (value := request.GET.get(option.field)):
                    continue
                condition[option.field] = value
        return condition

    @property
    def _get_urls(self):
        return re_path(f'{self.cls_name}/$', self._wrapper(self.read), name=self._get_full_name(self.cls_name))

