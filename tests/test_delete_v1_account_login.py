import structlog

from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_delete_v1_account_login():
    api = Facade(host='http://5.63.153.31:5051')
    orm = OrmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')
    login = "user_34"
    password = "user_34%"

    orm.delete_user_by_login(login=login)
    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.account.register_new_user(
        login="user_34",
        email="user_34@user_34",
        password="user_34%"
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
    api.login.set_headers(headers=token)
    api.login.logout_user()
    orm.db.close_connection()
