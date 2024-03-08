import structlog
from services.dm_api_account import Facade
from generic.helpers.orm_db import OrmDatabase

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_post_v1_account_password():
    api = Facade(host='http://5.63.153.31:5051')
    orm = OrmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')

    login = "user_39"
    password = "user_39%"
    email = "user_39@user_39"

    orm.delete_user_by_login(login=login)
    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.account.register_new_user(
        login="user_39",
        email="user_39@user_39",
        password="user_39%"
    )

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Login == login, f'User {login} not registered'
        assert row.Activated is False, f'User {login} was activated'

    orm.update_activation_status(login=login, activation_status=True)

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert row.Activated is True, f'User {login} is not activated'

    token = api.login.get_auth_token(login=login, password=password)
    api.account.set_headers(headers=token)
    api.account.reset_user_password(login=login, email=email, status_code=200)
    orm.db.close_connection()

