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


def test_get_v1_account():
    api = Facade(host='http://5.63.153.31:5051')
    login = "user_30"
    password = "user_30%"
    api.account.register_new_user(
        login="user_30",
        email="user_30@user_30",
        password="user_30%"
    )
    api.account.activate_registered_user(login=login)

    token = api.login.get_auth_token(login=login, password=password)
    api.account.set_headers(headers=token)
    api.login.set_headers(headers=token)
    response = api.account.get_current_user_info()
    assert_that(
        response.resource, has_properties(
            {
                "login": login,
                "roles": [UserRole.guest, UserRole.player],
                "rating": Rating(enabled=True, quality=0, quantity=0)
            }
        )
    )
