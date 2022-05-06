from django.urls import re_path
from web.views import account

app_name = 'signin'

urlpatterns = [
    re_path(r'^signin/', account.sign_in, name='signin'),
    re_path(r'^logout/', account.logout, name='logout'),
    re_path(r'^index/', account.index, name='index'),
   ]
