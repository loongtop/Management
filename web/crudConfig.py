"""Models for create the URLs"""
from django.urls import re_path

from crud import get_site, model_handler_tuple, name_tuple
from web.views import (employee, department, course,
                       customer, classTable, school, student,)
from web.models import (Employee, Department, Course,
                        Customer, ClassList, School, Student, )

model_handlers = (model_handler_tuple(Employee, employee.handler),
                  model_handler_tuple(Department, department.handler),
                  model_handler_tuple(Course, course.handler),
                  model_handler_tuple(Customer, customer.handler),
                  model_handler_tuple(ClassList, classTable.handler),
                  model_handler_tuple(School, school.handler),
                  model_handler_tuple(Student, student.handler), )


def urls(namespace, app_name="CRUD"):
    """
    generate the urls for web application to the project
    """
    site = get_site()
    site.set_name(name_tuple(namespace, app_name))
    site.register(model_handlers)
    return [re_path('', site.urls)]
