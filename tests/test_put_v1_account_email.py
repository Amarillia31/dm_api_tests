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
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_put_v1_account_email():
    api = Facade(host='http://5.63.153.31:5051')

    login = "user_42"
    password = "user_42%"
    email = "user_42_rpl@user_42"
    api.account.register_new_user(
        login="user_42",
        email="user_42@user_42",
        password="user_42%"
    )
    api.account.activate_registered_user(login=login)

    token = api.login.get_auth_token(login=login, password=password)
    api.account.set_headers(headers=token)
    response = api.account.change_registered_user_email(login=login, password=password, email=email)

    assert_that(
        response.resource, has_properties(
            {
                "login": "user_42",
                "roles": [UserRole.guest, UserRole.player],
                "rating": Rating(enabled=True, quality=0, quantity=0)
            }
        )
    )
