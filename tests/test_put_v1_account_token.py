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


def test_put_v1_account_token():
    api = Facade(host='http://5.63.153.31:5051')

    login = "user_40"
    api.account.register_new_user(
        login="user_40",
        email="user_40@user_40",
        password="user_40%"
    )
    response = api.account.activate_registered_user(login=login)

    assert_that(response.resource, has_properties({
        "login": "user_40",
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))

