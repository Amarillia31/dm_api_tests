import structlog

from dm_api_account.models.change_email_model import ChangeEmail
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.user_envelope_model import (
    UserRole,
    Rating,
)
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
from hamcrest import assert_that, has_properties

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_put_v1_account_email():
    api = DmApiAccount(host='http://5.63.153.31:5051')
    mailhog = MailhogApi(host="http://5.63.153.31:5025")
    json_replace = ChangeEmail(
        login="user_25",
        password="user_25%",
        email="user_25_rpl@user_25"
    )
    json_initial_user = Registration(
        login="user_25",
        email="user_25@user_25",
        password="user_25%"
    )
    user = api.account.post_v1_account(json=json_initial_user)

    token = mailhog.get_token_from_last_email()
    token_response = api.account.put_v1_account_token(
        token=token
    )

    response = api.account.put_v1_account_email(
        json=json_replace
    )
    assert_that(response.resource, has_properties({
        "login": "user_25",
        "roles": [UserRole.guest, UserRole.player],
        "rating": Rating(enabled=True, quality=0, quantity=0)
    }))

