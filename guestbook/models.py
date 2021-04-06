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


def findall():  # 리스트를 보여주는 함수
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor(DictCursor)  # db를 보고 결과를 딕셔너리로 줘라. [{'칼럼이름' : '값'}, {'칼럼이름' : '값'}]

        # SQL 실행
        sql = '''
          select no,
	             name,
                 message,
                 date_format(reg_date, "%Y-%m-%d %p %h:%i:%s") as reg_date
                 from guestbook
                 order by reg_date desc'''
        cursor.execute(sql)  # 위에서 알려준 sql 쿼리문으로 실행시켜라

        # 결과 받아오기
        results = cursor.fetchall()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환 ( 출력은 app.py 에서 해줄거니까, 결과값을 반환만 해준다)
        return results

    except OperationalError as e:  # 예외처리 (try ~ except 구문)
        print(f'error: {e}')


def insert(name, password, message): # 입력값을 db에 추가시켜주는 함수
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()  # 기본커서

        # SQL 실행
        sql = 'insert into guestbook values(null, %s, %s, %s, now())'
        count = cursor.execute(sql, (name, password, message))  # sql실행 성공하면 count =  True(1), 실패하면 False(0)이 된다.

        # commit
        db.commit()  # insert, update, delete 후에는 꼭 commit을 해 줘야 적용이 된다.

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 보기
        return count == 1  # True or False

    except OperationalError as e:
        print(f'error: {e}')


def deleteby_no_and_password(no, password):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()  # 기본커서

        # SQL 실행
        sql = 'delete from guestbook where no = %s and password = %s'
        count = cursor.execute(sql, (no, password))  # 입력값이 email 하나이므로, 튜플로 받기위해 괄호로 감싸고 콤마 하나 찍어줌

        # commit
        db.commit()  # insert, update, delete 후에는 꼭 commit을 해 줘야 적용이 된다.

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 보기
        return count == 1

    except OperationalError as e:
        print(f'error: {e}')