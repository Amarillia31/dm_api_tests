import structlog

from dm_api_account.models.registration_model import RegistrationModel
from dm_api_account.models.reset_password_model import ResetPasswordModel
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_post_v1_account_password():
    mailhog = MailhogApi(host="http://5.63.153.31:5025")
    api = DmApiAccount(host='http://5.63.153.31:5051')
    json_initial_user = RegistrationModel(
        login="user_21",
        email="user_21@user_21",
        password="user_21%"
    )
    user = api.account.post_v1_account(json=json_initial_user)
    assert user.status_code == 201, f'Expected status code 201, actual status code {user.status_code}'

    token = mailhog.get_token_from_last_email()
    token_response = api.account.put_v1_account_token(token=token)
    assert token_response.status_code == 200, f'Expected status code 200, ' \
                                              f'actual status code {token_response.status_code}'

    reset_json = ResetPasswordModel(
        login="user_21",
        email="user_21@user_21"
    )
    response = api.account.post_v1_account_password(
        json=reset_json
    )
    assert response.status_code == 200, f'Expected status code 200, actual status code {response.status_code}'
    #добавить получение токена после сброса пароля
