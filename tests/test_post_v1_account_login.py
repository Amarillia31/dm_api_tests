import structlog

from dm_api_account.models.login_credentials_model import LoginCredentials
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.user_envelope_model import (
    UserRole,
    Rating,
)
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
from hamcrest import (
    assert_that,
    has_properties,
)

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_post_v1_account_login():
    mailhog = MailhogApi(host="http://5.63.153.31:5025")
    api = DmApiAccount(host='http://5.63.153.31:5051')
    json_login = LoginCredentials(
        login="user_24",
        password="user_24%",
        rememberMe=True
    )
    json_initial_user = Registration(
        login="user_24",
        email="user_24@user_24",
        password="user_24%"
    )
    user = api.account.post_v1_account(json=json_initial_user)

    token = mailhog.get_token_from_last_email()
    token_response = api.account.put_v1_account_token(
        token=token
    )

    response = api.login.post_v1_account_login(
        json=json_login
    )

    assert_that(
        response.resource, has_properties(
            {
                "login": "user_24",
                "roles": [UserRole.guest, UserRole.player],
                "rating": Rating(enabled=True, quality=0, quantity=0)
            }
        )
    )
