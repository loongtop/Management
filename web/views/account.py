from django.shortcuts import redirect, render
from django.core.handlers.wsgi import WSGIRequest
from web.models import Employee
from django.http import HttpResponse

from rbac.utils.init_rbac import init_permission
from rbac.utils.encryption_md5 import encryption_str


def sign_in(request: WSGIRequest):
    """
    sign_in
    :param request:
    :return:
    """

    if request.method == 'GET':
        return render(request, 'signin.html')

    name = request.POST.get('name')
    password = encryption_str(request.POST.get('password', ''))

    if not (user := Employee.objects.filter(name=name, password=password).first()):
        return render(request, 'signin.html', {'msg': 'wrong user name or password'})

    init_permission(request, user)

    return redirect('/index/')


def logout(request):
    """
    logout
    :param request:
    :return:
    """
    request.session.delete()

    return redirect('/sign_in/')

def index(request):
    return render(request, 'index.html',)
