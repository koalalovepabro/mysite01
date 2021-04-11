desc board;

-- 게시글 작성 (insert)
-- insert into board values(null, '첫번째 게시글', '내용은 여기에 이렇게 들어갑니다.', '777', now(), '1', '1', '0', '3');
-- insert into board values(null, '두번째 게시글', '내용은 여기에 이렇게 들어갑니다.', '777', now(), '2', '1', '0', '2');
-- insert into board values(null, '세번째 게시글', '내용은 여기에 이렇게 들어갑니다.', '777', now(), '1', '2', '1', '1');

-- list
select * from board;
select * from user;

-- join으로 작성자 이름 알아내기
select a.name
from user a
join board b
on a.no = b.user_no
order by a.name;


