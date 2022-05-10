from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.urls import re_path

from crud import (CRUDSite,
                  model_handler_tuple, return_url, name_tuple,
                  HandlerList, Handler, RetrieveView, CreateView, DeleteView, DetailView, UpdateView,
                  func, StyleModelForm, Option,
                  mark_safe, pagination)


class StudentConfig(RetrieveView):
    pass

###################################


handlerList = HandlerList(retrieve=StudentConfig)
handler = handlerList.handler_dict

