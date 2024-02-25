import structlog

from dm_api_account.models.registration_model import Registration
from dm_api_account.models.reset_password_model import ResetPassword
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_post_v1_account_password():
    mailhog = MailhogApi(host="http://5.63.153.31:5025")
    api = DmApiAccount(host='http://5.63.153.31:5051')
    json_initial_user = Registration(
        login="user_21",
        email="user_21@user_21",
        password="user_21%"
    )
    user = api.account.post_v1_account(json=json_initial_user)

    token = mailhog.get_token_from_last_email()
    token_response = api.account.put_v1_account_token(token=token)

    reset_json = ResetPassword(
        login="user_21",
        email="user_21@user_21"
    )
    response = api.account.post_v1_account_password(
        json=reset_json,
        status_code=200
    )
    # добавить получение токена после сброса пароля
