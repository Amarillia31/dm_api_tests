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

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_password():
    api = Facade(host='http://5.63.153.31:5051')

    login = "user_33"
    password = "user_33%"
    new_password = "user_33%!"
    email = "user_33@user_33"
    api.account.register_new_user(
        login="user_33",
        email="user_33@user_33",
        password="user_33%"
    )
    api.account.activate_registered_user(login=login)

    token = api.login.get_auth_token(login=login, password=password)
    api.account.set_headers(headers=token)
    api.account.reset_user_password(login=login, email=email, status_code=200)
    response = api.account.change_user_password(login=login, old_password=password, new_password=new_password)

    assert_that(
        response.resource, has_properties(
            {
                "login": "user_33",
                "roles": [UserRole.guest, UserRole.player],
                "rating": Rating(enabled=True, quality=0, quantity=0)
            }
        )
    )
