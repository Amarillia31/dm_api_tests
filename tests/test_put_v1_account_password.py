from dm_api_account.models import Registration, ChangePassword, ResetPassword
from dm_api_account.models.user_envelope_model import UserRole, Rating
from services.dm_api_account import DmApiAccount
from hamcrest import assert_that, has_properties
from services.mailhog import MailhogApi
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_password():
    api = DmApiAccount(host='http://5.63.153.31:5051')
    mailhog = MailhogApi(host='http://5.63.153.31:5025')
    json_init_user = Registration(
        login="user_26",
        email="user_26@user_26",
        password="user_26%"
    )
    response = api.account.post_v1_account(json=json_init_user)
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token)

    reset_password_json = ResetPassword(
        login="user_26",
        email="user_26@user_26"
    )
    api.account.post_v1_account_password(json=reset_password_json, status_code=200)
    token = mailhog.get_token_from_last_email()
# нужно доработать функцию для получения токена после ресета  пароля, после этодого дописать тест
    json = ChangePassword(
        login="user_26",
        token=token,
        oldPassword="user_26%",
        newPassword="user_26%!"
    )

    response = api.account.put_v1_account_password(
        json=json
    )
    assert_that(
        response.resource, has_properties(
            {
                "login": "user_26",
                "roles": [UserRole.guest, UserRole.player],
                "rating": Rating(enabled=True, quality=0, quantity=0)
            }
        )
    )
