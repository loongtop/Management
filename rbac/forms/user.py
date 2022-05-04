from django import forms
from rbac import models

from django.core.exceptions import ValidationError


class UserModelForm(forms.ModelForm):
    """UserModelForm"""
    confirm_password = forms.CharField(label='confirmed password')

    class Meta:
        model = models.User
        fields = ['name', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        """
        Check if the password is the same
        :return:
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('the tow passwords not the same!')
        return confirm_password


class ResetPasswordUserModelForm(forms.ModelForm):
    """ResetPassword for UserModelForm"""
    confirm_password = forms.CharField(label='Confirmed password')

    class Meta:
        model = models.User
        fields = ['password', 'confirm_password']

    def __init__(self):
        super(ResetPasswordUserModelForm, self).__init__(*arg, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        """check the password"""
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise ValidationError('The two passwords are different!')
        return confirm_password