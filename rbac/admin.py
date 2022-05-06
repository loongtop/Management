from django.contrib import admin
from rbac.models import Menu, Permission, Role
from web.models import Employee

# Register your models here.

admin.site.register(Employee)
admin.site.register(Menu)
admin.site.register(Permission)
admin.site.register(Role)