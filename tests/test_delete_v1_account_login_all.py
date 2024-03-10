import structlog
from hamcrest import (
    assert_that,
    has_entries,
)

from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_delete_v1_account_login_all(facade, orm, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert_that(
            row, has_entries(
                {
                    'Login': login,
                    'Activated': False
                }
            )
        )

    orm.update_activation_status(login=login, activation_status=True)

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert_that(row, has_entries(
            {
                'Activated': True
            }
        ))

    token = facade.login.get_auth_token(login=login, password=password)
    facade.login.set_headers(headers=token)
    facade.login.logout_user_from_all_devices()
