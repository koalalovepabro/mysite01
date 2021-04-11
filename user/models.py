from django.db import models

from MySQLdb import connect, OperationalError
from MySQLdb.cursors import DictCursor


def conn():
    return connect(  # db는 객체가 저장 되어있는 주소를 나타냄.
        user='webdb',
        password='webdb',
        host='localhost',
        port=3306,
        db='webdb',
        charset='utf8')


def findbyno(no):  # 이름, 이메일, 성별을 updateform 에 뿌려줌
    # 연결
    db = conn()

    # cursor 생성
    cursor = db.cursor(DictCursor)  # db를 보고 결과를 딕셔너리로 줘라. [{'칼럼이름' : '값'}, {'칼럼이름' : '값'}]

    # SQL 실행
    sql = 'select name, email, gender, password from user where no = %s'
    cursor.execute(sql, (no,))  # 위에서 알려준 sql 쿼리문으로 실행시켜라

    # 결과 받아오기
    result = cursor.fetchone()  # 결과를 하나만 받아올 때에는, fetchall()이 아니라 fetchone() 으로 해줌

    # 자원 정리
    cursor.close()
    db.close()

    # 결과 반환 ( 출력은 app.py 에서 해줄거니까, 결과값을 반환만 해준다)
    return result


def findby_email_and_password(email, password):  # 로그인하는 함수
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor(DictCursor)  # db를 보고 결과를 딕셔너리로 줘라. [{'칼럼이름' : '값'}, {'칼럼이름' : '값'}]

        # SQL 실행
        sql = 'select no, name from user where email=%s and password =%s'
        cursor.execute(sql, (email, password))  # 위에서 알려준 sql 쿼리문으로 실행시켜라

        # 결과 받아오기
        result = cursor.fetchone()  #결과를 하나만 받아올 때에는, fetchall()이 아니라 fetchone() 으로 해줌

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환 ( 출력은 app.py 에서 해줄거니까, 결과값을 반환만 해준다)
        return result

    except OperationalError as e:  # 예외처리 (try ~ except 구문)
        print(f'error: {e}')


def insert(name, email, password, gender): # 입력값을 db에 추가시켜주는 함수
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()  # 기본커서

        # SQL 실행
        sql = 'insert into user values(null, %s, %s, %s, %s, now())'
        count = cursor.execute(sql, (name, email, password, gender))  # sql실행 성공하면 count =  True(1), 실패하면 False(0)이 된다.

        # commit
        db.commit()  # insert, update, delete 후에는 꼭 commit을 해 줘야 적용이 된다.

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 보기
        return count == 1  # True or False

    except OperationalError as e:
        print(f'error: {e}')


def update(name, password, gender, no):  # 과제(2021.04.07)
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()  # 기본커서

        # SQL 실행
        sql = 'update user set name=%s, password=%s, gender=%s where no =%s'
        count = cursor.execute(sql, (name, password, gender, no))  # sql실행 성공하면 count =  True(1), 실패하면 False(0)이 된다.

        # commit
        db.commit()  # insert, update, delete 후에는 꼭 commit을 해 줘야 적용이 된다.

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 보기
        return count == 1  # True or False

    except OperationalError as e:
        print(f'error: {e}')