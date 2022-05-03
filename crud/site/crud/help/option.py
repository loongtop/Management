from django.db.models import ForeignKey, ManyToManyField

from .searchGroupRow import SearchGroupRow


class Option(object):
    def __init__(self, field, is_multi=False, db_condition=None, text_func=None, value_func=None):
        """
        :param field: the field associated with the combined search
        :param is_multi: Whether to support multiple selection
        :param db_condition: the condition of database association query
        :param text_func: This function is used to display the combined search button page text
        :param value_func: This function is used to display the combined search button value
        """
        self.field = field
        self.is_multi = is_multi
        # if not db_condition:
        #     db_condition = {}
        # self.db_condition = db_condition
        self.db_condition = db_condition if db_condition else {}
        self.text_func = text_func
        self.value_func = value_func

        self.is_choice = False

    def get_db_condition(self, request, *args, **kwargs):
        return self.db_condition

    def get_queryset_or_tuple(self, model, request, *args, **kwargs):
        """
        Get the data associated with the database according to the field
        :return:
        """
        field_object = model._meta.get_field(self.field)
        title = field_object.verbose_name
        # Get relevant data
        if isinstance(field_object, ForeignKey) or isinstance(field_object, ManyToManyField):
            # FK and M2M should get the data in their associated tables: QuerySet
            db_condition = self.get_db_condition(request, *args, **kwargs)
            return SearchGroupRow(title, field_object.remote_field.model.objects.filter(**db_condition), self, request.GET)
        else:
            # Get data in choice: tuple
            self.is_choice = True
            return SearchGroupRow(title, field_object.choices, self, request.GET)

    def get_text(self, field_object):
        """
        :param field_object:
        :return:
        """
        if self.text_func:
            return self.text_func(field_object)

        if self.is_choice:
            return field_object[1]

        return str(field_object)

    def get_value(self, field_object):
        """
        :param field_object:
        :return:
        """
        if self.value_func:
            return self.value_func(field_object)

        if self.is_choice:
            return field_object[0]

        return field_object.pk
