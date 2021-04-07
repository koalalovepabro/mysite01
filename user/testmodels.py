from user import models


def test_models_insert():  # 회원가입(join)
    models.insert('희동이', 'baby@gmail.com', '333', 'male')

def test_models_findby_email_and_password():
    result = models.findby_email_and_password('baby@gmail.com', '333')
    print(result)


# test_models_insert()
test_models_findby_email_and_password()
