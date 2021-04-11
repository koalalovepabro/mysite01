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


def findall(page=1, listcount=10, kwd=''):  # 리스트를 보여주는 함수
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor(DictCursor)  # db를 보고 결과를 딕셔너리로 줘라. [{'칼럼이름' : '값'}, {'칼럼이름' : '값'}]

        # SQL 실행
        # kwd 있을 때
        if kwd is not None and len(kwd) > 1:
            sql = '''
                  select t1.no
                        , t1.title
                        , t2.name 
                        , t1.hit
                        , t1.reg_date
                        , t1.g_no
                        , t1.o_no
                        , t1.depth
                        , t1.user_no
                    from board t1 JOIN user t2 ON (t1.user_no = t2.no)
                   where t1.title like concat('%%', %s, '%%')
                ORDER BY t1.g_no DESC, t1.o_no ASC
                   limit %s, %s'''
            cursor.execute(sql, (kwd, page, listcount))  # 위에서 알려준 sql 쿼리문으로 실행시켜라

        # kwd 없을 때
        else:

            sql = '''
                  select t1.no
                        , t1.title
                        , t2.name 
                        , t1.hit
                        , t1.reg_date
                        , t1.g_no
                        , t1.o_no
                        , t1.depth
                        , t1.user_no
                    from board t1 JOIN user t2 ON (t1.user_no = t2.no)
                ORDER BY t1.g_no DESC, t1.o_no ASC
                   limit %s, %s'''
            cursor.execute(sql, (page, listcount))  # 위에서 알려준 sql 쿼리문으로 실행시켜라

        # SQL 실행
        # sql = '''
        #     select no,
        #            title,
        #            (select name
        #               from user
        #              where no = board.user_no) as writer,
        # '''

        # 결과 받아오기
        results = cursor.fetchall()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환 ( 출력은 app.py 에서 해줄거니까, 결과값을 반환만 해준다)
        return results

    except OperationalError as e:  # 예외처리 (try ~ except 구문)
        print(f'error: {e}')


def count(kwd=''):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor(DictCursor)  # db를 보고 결과를 딕셔너리로 줘라. [{'칼럼이름' : '값'}, {'칼럼이름' : '값'}]

        # SQL 실행
        sql = 'select count(*) as c from board'

        # kwd 있을 때
        if kwd is not None and len(kwd) > 1:
            sql += 'where title like concat("%%", %s, "%%")'
            cursor.execute(sql, (kwd, ))

        # kwd 없을 때
        else:
            cursor.execute(sql)

        # 결과 받아오기
        result = cursor.fetchone()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 보기
        return result['c']

    except OperationalError as e:
        print(f'error: {e}')


def hit(post_no):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()  # 기본커서

        # SQL 실행
        sql = '''update board set
                        hit = hit + 1
                  where no = %s
              '''
        count = cursor.execute(sql, (post_no,))  # 입력값이 하나이므로, 튜플로 받기위해 괄호로 감싸고 콤마 하나 찍어줌

        # commit
        db.commit()  # insert, update, delete 후에는 꼭 commit을 해 줘야 적용이 된다.

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 보기
        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


def find(post_no):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor(DictCursor)  # db를 보고 결과를 딕셔너리로 줘라. [{'칼럼이름' : '값'}, {'칼럼이름' : '값'}]

        # SQL 실행
        sql = '''
            select no, title, contents, hit, reg_date, g_no, o_no, depth, user_no
              from board 
             where no = %s 
             limit 1'''

        cursor.execute(sql, (post_no,))

        # 결과 받아오기
        result = cursor.fetchone()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 보기
        return result

    except OperationalError as e:
        print(f'error: {e}')


def insert(data):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()  # 기본커서

        # SQL 실행
        sql = '''
                insert into board(no, title, contents, hit, reg_date, g_no, o_no, depth, user_no) values(
                                  null, %s, %s, 0, now(), ifnull((select max(a.g_no) from board as a),0) +1, 1, 0, %s)'''

        result = cursor.execute(sql, (data['title'], data['contents'], data['user_no']))

        # commit
        db.commit()  # insert, update, delete 후에는 꼭 commit을 해 줘야 적용이 된다.

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 보기
        return result == 1

    except OperationalError as e:
        print(f'error: {e}')

def update(data):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()  # 기본커서

        # SQL 실행
        sql = 'update board set title = %s, contents = %s where no = %s'

        count = cursor.execute(sql, (data['title'], data['contents'], data['no']))  # 입력값이 email 하나이므로, 튜플로 받기위해 괄호로 감싸고 콤마 하나 찍어줌

        # commit
        db.commit()  # insert, update, delete 후에는 꼭 commit을 해 줘야 적용이 된다.

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 보기
        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


def delete(post_no):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()  # 기본커서

        # SQL 실행
        sql = 'delete from board where no = %s'
        count = cursor.execute(sql, (post_no,))  # 입력값이 email 하나이므로, 튜플로 받기위해 괄호로 감싸고 콤마 하나 찍어줌

        # commit
        db.commit()  # insert, update, delete 후에는 꼭 commit을 해 줘야 적용이 된다.

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 보기
        return count == 1

    except OperationalError as e:
        print(f'error: {e}')

def reply(data):
    result = 0
    try:
        # 연결
        db = conn()

        try:

            # cursor 생성 (o_no 업데이트)
            cursor = db.cursor()

            # SQL 실행
            sql = '''
                update board 
                   set o_no = o_no + 1
                 where g_no = %s and o_no >= %s'''

            result = cursor.execute(sql, (data['g_no'], data['o_no']))

            # cursor 생성 (reply 저장)
            cursor = db.cursor()
            # SQL 실행
            sql = '''
                insert into board( no, title, contents, hit, reg_date, g_no, o_no, depth, user_no)
                           values( null, %s, %s, 0, now(), %s, %s, %s, %s)'''

            result = cursor.execute(sql, (data['title'], data['contents'], data['g_no'], data['o_no'], data['depth'], data['user_no']))

            # commit
            db.commit()  # insert, update, delete 후에는 꼭 commit을 해 줘야 적용이 된다.

            # 자원 정리
            cursor.close()


        # o_no 업데이트, reply 저장에 대한 오류
        except Exception as e:
            print(f'error: {e}')
            db.rollback()  # Transaction. 둘다 제대로 안됐으면 없던일로 돌려놓기 !

        db.close() # Transaction(commit & rollback) 까지 완료 한 후에 db 닫기

       # 결과 보기
        return result == 1

    # DB연결에 대한 오류처리
    except OperationalError as e:
        print(f'error: {e}')

