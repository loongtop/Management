from django.urls import re_path, include
from django.contrib import admin
from rbac.view import user, role, permission, menu

app_name = 'rbac'

urlpatterns = [
    # re_path(r'^user/list/$', user.UserListView.as_view(), name='user_list'),
    # re_path(r'^user/create/$', user.UserCreateView.as_view(), name='user_create'),
    # re_path(r'^user/update/(?P<pk>\d+)/$', user.UserUpdateView.as_view(), name='user_update'),
    # re_path(r'^user/del/(?P<pk>\d+)/$', user.UserDeleteView.as_view(), name='user_del'),
    # re_path(r'^user/reset/password/(?P<pk>\d+)/$', user.ResetPasswordView.as_view(), name='user_reset_pwd'),

    # re_path(r'^role/list/$', role.role_list, name='role_list'),  # rbac:role_list
    # re_path(r'^role/create/$', role.role_create, name='role_create'),  # rbac:role_createa
    # re_path(r'^role/update/(?P<pk>\d+)/$', role.role_update, name='role_update'),  # rbac:role_update
    # re_path(r'^role/del/(?P<pk>\d+)/$', role.role_del, name='role_del'),  # rbac:role_del

    # re_path(r'^menu/list/$', menu.menu_list, name='menu_list'),
    # re_path(r'^menu/create/$', menu.menu_create, name='menu_create'),
    # re_path(r'^menu/update/(?P<pk>\d+)/$', menu.menu_update, name='menu_update'),
    # re_path(r'^menu/del/(?P<pk>\d+)/$', menu.menu_del, name='menu_del'),
    #
    # re_path(r'^second/menu/create/(?P<menu_id>\d+)$', menu.second_menu_create, name='second_menu_create'),
    # re_path(r'^second/menu/update/(?P<pk>\d+)/$', menu.second_menu_update, name='second_menu_update'),
    # re_path(r'^second/menu/del/(?P<pk>\d+)/$', menu.second_menu_del, name='second_menu_del'),
    #
    # re_path(r'^permission/create/(?P<second_menu_id>\d+)/$', permission.permission_create, name='permission_create'),
    # re_path(r'^permission/update/(?P<pk>\d+)/$', permission.permission_update, name='permission_update'),
    # re_path(r'^permission/del/(?P<pk>\d+)/$', permission.permission_del, name='permission_del'),
    #
    # re_path(r'^multi/permissions/$', permission.multi_permissions, name='multi_permissions'),
    # re_path(r'^multi/permissions/del/(?P<pk>\d+)/$', permission.multi_permissions_del, name='multi_permissions_del'),
    #
    # re_path(r'^distribute/permissions/$', permission.distribute_permissions, name='distribute_permissions'),
]
