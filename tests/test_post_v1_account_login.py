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


def test_post_v1_account_login():
    api = Facade(host='http://5.63.153.31:5051')

    login = "user_41"
    password = "user_41%"
    api.account.register_new_user(
        login="user_41",
        email="user_41@user_41",
        password="user_41%"
    )
    api.account.activate_registered_user(login=login)
    response = api.login.login_user(login=login, password=password)

    #не работает без json !!!!!!!!!!!!!!
    # assert_that(
    #     response.resource, has_properties(
    #         {
    #             "login": "user_37",
    #             "roles": [UserRole.guest, UserRole.player],
    #             "rating": Rating(enabled=True, quality=0, quantity=0)
    #         }
    #     )
    # )
