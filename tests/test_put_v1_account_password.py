import structlog
from hamcrest import (
    assert_that,
    has_properties,
)

from dm_api_account.models.user_envelope_model import (
    UserRole,
    Rating,
)
from services.dm_api_account import Facade
from generic.helpers.orm_db import OrmDatabase

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_password():
    api = Facade(host='http://5.63.153.31:5051')
    orm = OrmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')

    login = "user_50"
    password = "user_50%"
    new_password = "user_50%!"
    email = "user_50@user_50"

    orm.delete_user_by_login(login=login)
    dataset = orm.get_user_by_login(login=login)
    assert len(dataset) == 0

    api.mailhog.delete_all_messages()

    api.account.register_new_user(
        login="user_50",
        email="user_50@user_50",
        password="user_50%"
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
    response = api.account.change_user_password(login=login, old_password=password, new_password=new_password)

    assert_that(
        response.resource, has_properties(
            {
                "login": "user_50",
                "roles": [UserRole.guest, UserRole.player],
                "rating": Rating(enabled=True, quality=0, quantity=0)
            }
        )
    )
    orm.db.close_connection()
