from math import ceil

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from board import models

LIST_COUNT = 10     # 한 페이지당 리스트를 10개 보여준다는 뜻
                    # findall()로 이 값을 넘겨줘야 함.


def index(request):
    page = int(request.GET.get('p', '1'))

    # 키워드 유/무 조건
    if 'kwd' in request.GET:
        kwd = request.GET.get('kwd', '')
    else:
        kwd = ''

    # 없는 페이지는 흐린 글씨로 표시
    index = (page -1) * LIST_COUNT
    page_numbers_range = 5   # 게시판 화면에서 표시할 페이징 범위의 크기
    results = models.findall(index, LIST_COUNT, kwd)  # 게시판 페이지마다 보이는 글(LIST)

    totalcount = models.count(kwd)            # 글의 총 갯수(LIST 갯수)
    pagecount = ceil(totalcount/LIST_COUNT)   # 글의 총 갯수를 페이지당 보여질 글의 갯수로 나눈 몫에서 1을 더함(반올림)
    # pagecount = ceil(totalcount / LIST_COUNT)   # 글의 총 갯수를 페이지당 보여질 글의 갯수로 나눈 몫에서 1을 더함(반올림)

    curpage = page                            # 현재 페이지

    nextpage = curpage + 1 if curpage < pagecount else curpage
    # 현재 페이지가 총 페이지수보다 작으면 1을 더하고, 아니면 현재 페이지로 표시하기

    prevpage = 1 if (curpage - 1) < 1 else curpage-1
    # 현재페이지가 1페이지인 경우 다음 페이지는 1이며, 그게 아니라면 현재페이지-1이 이전페이지.

    start_index = int((curpage - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    pager = {
        "totalcount": totalcount,  # 글의 총 갯수(LIST 갯수)
        "listcount": LIST_COUNT,   # 한 페이지당 보여줄 리스트 갯수
        "pagecount": pagecount,    # 페이지의 총 갯수 (totalcount를 LIST_COUNT로 나눈 몫에서 1을 더함)
        "nextpage": nextpage,      # nextpage로 넘어가는 링크 줌. nextpage가 5보다 크면, 다음 페이지로 넘어가는 화살표 표시에 링크 줌.
        "prevpage": prevpage,      # prevpage로 넘어가는 링크 줌. prevpage가 4보다 크면, 이전 페이지로 넘어가는 화살표 표시에 링크 줌.
        "curpage": curpage,        # 현재페이지를 빨간색으로 강조표시(링크는 안줌)
        "paging": range(start_index+1, end_index+1),    # 게시판 화면에서 페이징 범위
    }

    # 글 시작 번호
    startcount = totalcount - (curpage - 1) * LIST_COUNT
    print(startcount)

    data = {
        "startcount": startcount,
        "board_list": results,      # 전체 리스트. findall()의 결과
        "keyword": kwd,
        "pager": pager
    }

    return render(request, 'board/index.html', data)

    # 페이징 -> 리스트 출력 구현 한 후에 해보기 !!

    # page = request.GET.get('p')
    # print(type(page))  # class 'str'으로 출력됨
    #
    # page = 1 if page is None else int(page)
    # print(page) # http://localhost:9999/board/?p=10 에서 10이 출력됨

    # page = request.GET['p']
    # boardlist = models.findall(page, LIST_COUNT)
    #
    # data = {
    #     'boardlist': boardlist,
    # }

    # totalcount = models.count()     # 글의 총 갯수(LIST 갯수)
    # boardlist = models.findall(page, LIST_COUNT)  # 게시판 페이지마다 보이는 글(LIST)
    #
    # # paging 정보를 계산
    # pagecount = ceil(totalcount / LIST_COUNT)   # 글의 총 갯수를 페이지당 보여질 글의 갯수로 나눈 몫에서 1을 더함(반올림)
    #
    # data = {
    #     "boardlist" : boardlist, # 글의 총 갯수(LIST 갯수)
    #     "pagecount" : pagecount, # 페이지의 총 갯수 (totalcount를 LIST_COUNT로 나눈 몫에서 1을 더함)
    #     'nextpage' : 7,          # nextpage로 넘어가는 링크 줌. nextpage가 5보다 크면, 다음 페이지로 넘어가는 화살표 표시에 링크 줌.
    #     'prevpage' : 5,          # prevpage로 넘어가는 링크 줌. prevpage가 4보다 크면, 이전 페이지로 넘어가는 화살표 표시에 링크 줌.
    #     'curpage' : 2            # 현재페이지를 빨간색으로 강조표시(링크는 안줌)
    # }


# 게시판에서 글 제목 클릭 -> 글 읽기
def view(request):
    post_no = request.GET.get('no')   # board 테이블의 PK인 no (게시글 insert 할 때 자동 생성되는 값)

    # 없는 post_no를 임의로 접속하려고 할 때
    if post_no is None:
        return HttpResponse('존재하지 않는 게시글입니다.')
    result = models.find(post_no)

    # 게시글이 없을 경우
    if result is None:
        return HttpResponse('게시글을 찾을 수 없습니다.')

    data = {'post': result}

    # 조회수
    models.hit(post_no)
    return render(request, 'board/view.html', data)


# 글 쓰기- 폼
def writeform(request):
    authuser = request.session.get('authuser')

    # 로그아웃 상태
    if authuser is None:
        return HttpResponseRedirect('/')

    return render(request, 'board/writeform.html')


# 글 쓰기- 실행
def write(request):
    authuser = request.session.get('authuser')

    # 로그아웃 상태
    if authuser is None:
        return HttpResponseRedirect('/')

    title = request.POST['title']

    contents = request.POST['contents']

    data = {'user_no': authuser['no'], 'title': title, 'contents': contents}



    result = models.insert(data)

    # 모델 실행 오류
    if result != 1:
        return HttpResponse('Error')


    # 모델 정상 실행
    return HttpResponseRedirect('/board/')


def updateform(request):
    authuser = request.session.get('authuser')
    # 로그아웃 상태
    if authuser is None:
        return HttpResponseRedirect('/')

    post_no = request.GET.get('no')

    # 없는 post_no로 접속하려고 할 때
    if post_no is None:
        return HttpResponse('존재하지 않는 게시글입니다.')

    result = models.find(post_no)
    # find 모델 결과가 없을 경우
    if result is None:
        return HttpResponse('게시글을 찾을 수 없습니다.')

    # 작성자가 아닌데 url 입력해서 접속 한 경우
    if result['user_no'] != authuser['no']:
        return HttpResponse('수정 권한이 없습니다.')

    data = {"post": result}

    return render(request, 'board/updateform.html', data)

def update(request):
    authuser = request.session.get('authuser')
    # 로그아웃 상태
    if authuser is None:
        return HttpResponseRedirect('/')

    post_no = request.POST.get('no')

    # 없는 post_no로 접속하려고 할 때
    if post_no is None:
        return HttpResponse('존재하지 않는 게시글입니다.')

    result = models.find(post_no)
    # find 모델 결과가 없을 경우
    if result is None:
        return HttpResponse('게시글을 찾을 수 없습니다.')

    # 작성자가 아닌데 url 입력해서 접속 한 경우
    if result['user_no'] != authuser['no']:
        return HttpResponse('수정 권한이 없습니다.')

    title = request.POST['title']
    contents = request.POST['contents']

    data = {'title': title, 'contents': contents, 'no': post_no}
    models.update(data)

    return HttpResponseRedirect('/board')


def delete(request):
    authuser = request.session.get('authuser')
    # 로그아웃 상태
    if authuser is None:
        return HttpResponseRedirect('/')

    post_no = request.GET.get('no')

    # 없는 post_no를 임의로 접속하려고 할 때
    if post_no is None:
        return HttpResponse('존재하지 않는 게시글입니다.')

    result = models.find(post_no)
    # find 모델 결과가 없을 경우
    if result is None:
        return HttpResponse('게시글을 찾을 수 없습니다.')

    # 작성자가 아닌데 url 입력해서 접속 한 경우
    if result['user_no'] != authuser['no']:
        return HttpResponse('삭제 권한이 없습니다.')

    models.delete(post_no)

    return HttpResponseRedirect('/board')


def replyform(request):
    authuser = request.session.get('authuser')
    # 로그아웃 상태
    if authuser is None:
        return HttpResponseRedirect('/')

    post_no = request.GET.get('no')

    # 없는 post_no를 임의로 접속하려고 할 때
    if post_no is None:
        return HttpResponse('존재하지 않는 게시글입니다.')

    result = models.find(post_no)
    # find 모델 결과가 없을 경우
    if result is None:
        return HttpResponse('게시글을 찾을 수 없습니다.')

    data = {'post_for_reply': result }

    return render(request, 'board/replyform.html', data)

def reply(request):
    authuser = request.session.get('authuser')
    # 로그아웃 상태
    if authuser is None:
        return HttpResponseRedirect('/')

    title = request.POST['title']
    contents = request.POST['contents']

    g_no = request.POST['g_no']
    o_no = request.POST['o_no']
    depth = request.POST['depth']

    g_no = int(g_no)
    o_no = int(o_no) + 1
    depth = int(depth) + 1

    data = {
        'user_no': authuser['no'],
        'title': title,
        'contents': contents,
        'g_no': g_no,
        'o_no': o_no,
        'depth': depth
    }

    result = models.reply(data)

    # 모델 실행 오류
    if result != 1:
        return HttpResponse('Error')

    return HttpResponseRedirect('/board')