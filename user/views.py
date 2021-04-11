from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from user import models


def joinform(request):
    return render(request, 'user/joinform.html')


def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')


def join(request):
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    gender = request.POST['gender']

    models.insert(name, email, password, gender)

    return HttpResponseRedirect('/user/joinsuccess')


def loginform(request):
    return render(request, 'user/loginform.html')


def login(request):
    email = request.POST['email']
    password = request.POST['password']

    result = models.findby_email_and_password(email, password)

    if result is None:
        return HttpResponseRedirect('/user/loginform?result=fail')

    # login 처리
    request.session['authuser'] = result  # result(메모리)라는 딕셔너리 안에 인증받은유저인 'authuser' 이름이 저장됨. authuser가 있으면->로그인 된거, 없으면->로그인 안된거
    return HttpResponseRedirect('/')


def logout(request):
    del request.session['authuser']  # authuser 삭제
    return HttpResponseRedirect('/')


def updateform(request): # 회원정보 수정
    # Access Control (접근제어)
    authuser = request.session.get('authuser')
    if authuser is None:    # 로그인이 되어있지 않을때-> 메인화면으로 이동
        return HttpResponseRedirect('/')

    #authuser = request.session['authuser']
    results = models.findbyno(authuser['no'])  # findbyno 함수에서 찾은 값들을 results에 저장
    data = {'info': results}
    return render(request, 'user/updateform.html', data)


def update(request):
    authuser = request.session.get('authuser')
    no = authuser['no']

    name = request.POST['name']
    password = request.POST['password']
    gender = request.POST['gender']

    models.update(name, password, gender, no)

    return HttpResponseRedirect("/user/updatesuccess")

def updatesuccess(request):
    del request.session["authuser"]
    return render(request, 'user/updatesuccess.html')
