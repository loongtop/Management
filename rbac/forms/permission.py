
from django import forms
from django.utils.safestring import mark_safe
from rbac import models
from rbac.forms.bootstrap import BootStrapModelForm


class PermissionModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'url',]
