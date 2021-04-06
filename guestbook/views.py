from django.http import HttpResponseRedirect
from django.shortcuts import render

from guestbook import models


def index(request):
    results = models.findall()
    data = {"guestbook_list": results}

    return render(request, 'guestbook/index.html', data)


def add(request):
    name = request.POST['name']
    password = request.POST['pass']
    message = request.POST['content']

    models.insert(name, password, message)

    return HttpResponseRedirect("/guestbook")


def deleteform(request):
    return render(request, 'guestbook/deleteform.html')


def delete(request):
    no = request.POST['no']
    password = request.POST['password']

    models.deleteby_no_and_password(no, password)

    return HttpResponseRedirect("/guestbook")