class Option(object):
    def __init__(self, field, is_multi=False, db_condition=None, text_func=None, value_func=None):
        """
        :param field: 组合搜索关联的字段
        :param is_multi: 是否支持多选
        :param db_condition: 数据库关联查询时的条件
        :param text_func: 此函数用于显示组合搜索按钮页面文本
        :param value_func: 此函数用于显示组合搜索按钮值
        """
        self.field = field
        self.is_multi = is_multi
        if not db_condition:
            db_condition = {}
        self.db_condition = db_condition
        self.text_func = text_func
        self.value_func = value_func

        self.is_choice = False

    def get_db_condition(self, request, *args, **kwargs):
        return self.db_condition

    def get_queryset_or_tuple(self, model_class, request, *args, **kwargs):
        """
        Get the data associated with the database according to the field
        :return:
        """
        field_object = self._get_meta().get_field(self.field)
        title = field_object.verbose_name
        # Get relevant data
        if isinstance(field_object, ForeignKey) or isinstance(field_object, ManyToManyField):
            # FK and M2M should get the data in their associated tables: QuerySet
            db_condition = self.get_db_condition(request, *args, **kwargs)
            return SearchGroupRow(title, field_object.rel.model.objects.filter(**db_condition), self, request.GET)
        else:
            # Get data in choice: tuple
            self.is_choice = True
            return SearchGroupRow(title, field_object.choices, self, request.GET)

    def get_text(self, field_object):
        """
        获取文本函数
        :param field_object:
        :return:
        """
        if self.text_func:
            return self.text_func(field_object)

        if self.is_choice:
            return field_object[1]

        return str(field_object)

    def get_value(self, field_object):
        if self.value_func:
            return self.value_func(field_object)

        if self.is_choice:
            return field_object[0]

        return field_object.pk