from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from rbac import models


class UserListView(ListView):
    """UserListView"""
    model = models.User
    template_name = 'rbac/user_list.html'
    context_object_name = 'user_list'
    # Tell which request method is allowed
    http_method_names = ['GET']

    def get_context_data(self, *, object_list=None, **kwargs):
        """If more than one set of data is required to return Template,
            the get_context_data method needs to be rewritten"""
        context = super().get_context_data(**kwargs)
        user_name = self.request.GET.get('user', None)
        context['user'] = models.User.objects.get(username=user_name)

        # the context contains {'user_list': user_list, 'user': user}
        return context


class UserCreateView(CreateView):
    """UserCreateView"""
    model = models.User
    template_name = 'rbac/user_create.html'
    fields = ['name', 'password', 'email', 'role']
    success_url = reverse_lazy('rbac:user_list')


class UserUpdateView(UpdateView):
    """UserCreateView"""
    model = models.User
    template_name = 'rbac/user_update.html'
    fields = ['name', 'password', 'email', 'role']
    success_url = reverse_lazy('rbac:user_list')


class UserDeleteView(DeleteView):
    """UserDeleteView"""
    model = models.User
    template_name = 'rbac/user_delete.html'
    success_url = reverse_lazy('rbac:user_list')


def user_reset_pwd(request):
    pass

