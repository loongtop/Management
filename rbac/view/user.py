from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy

from web import models
from rbac.forms.user import ResetPasswordUserModelForm


class UserListView(ListView):
    """UserListView"""
    model = models.Employee
    template_name = 'rbac/user_list.html'
    context_object_name = 'user_list'
    # Tell which request method is allowed
    # http_method_names = ['GET', 'POST']


class UserCreateView(CreateView):
    """UserCreateView"""
    model = models.Employee
    template_name = 'rbac/change.html'
    fields = '__all__'
    success_url = reverse_lazy('rbac:user_list')


class UserUpdateView(UpdateView):
    """UserCreateView"""
    model = models.Employee
    template_name = 'rbac/change.html'
    fields = ['name', 'password', 'email', 'role', 'gender', 'department']
    success_url = reverse_lazy('rbac:user_list')


class UserDeleteView(DeleteView):
    """UserDeleteView"""
    model = models.Employee
    template_name = 'rbac/delete.html'
    success_url = reverse_lazy('rbac:user_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        """If more than one set of data is required to return Template,
            the get_context_data method needs to be rewritten"""

        context = super().get_context_data(**kwargs)
        context['cancel'] = reverse_lazy('rbac:user_list')

        # the context contains {'cancel': 'rbac:user_list'}
        return context


class ResetPasswordView(View):
    """ResetPasswordView"""

    def get(self, request):
        form = ResetPasswordUserModelForm()
        return render(request, 'rbac/change.html', {'from': form})
