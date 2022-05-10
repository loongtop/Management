from django.shortcuts import render, redirect
from django.urls import re_path
from django import forms
from django.core.exceptions import ValidationError

from crud import (CRUDSite,
                  model_handler_tuple, return_url, name_tuple,
                  HandlerList, Handler, RetrieveView, CreateView, DeleteView, DetailView, UpdateView,
                  func, StyleModelForm, Option,
                  mark_safe, pagination)


class EmployeeCFG(RetrieveView):
    """EmployeeCFG"""
    display_list = [func.detail, 'nickname', 'gender', 'phone', 'department', func.update_delete]

    search_list = ['nickname', 'gender']

    search_group = [
        Option(field='gender'),
        Option(field='department'),
    ]

    def reset_password_view(self, request, pk):
        """
        reset password view
        :param request:
        :param pk:
        :return:
        """
        if not (obj := self.is_obj_exists(pk=pk)):
            return None

        if request.method == 'GET':
            form = ResetPasswordForm()
            return render(request, 'crud/change.html', {'form': form})
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            obj.password = form.cleaned_data['password']
            obj.save()
            return redirect(self.reverse_list_url())
        return render(request, 'crud/change.html', {'form': form})

    @property
    def extra_urls(self):

        patterns = [re_path(r'reset/password/(?P<pk>\d+)/$',
                            self._wrapper(self.reset_password_view),
                            name=self._get_full_name('reset_pwd')), ]
        return patterns


class ResetPasswordForm(StyleModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmed password', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


handlerList = HandlerList(retrieve=EmployeeCFG)
handler = handlerList.handler_dict