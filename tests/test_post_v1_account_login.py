import structlog

from dm_api_account.models.login_credentials_model import LoginCredentialsModel
from dm_api_account.models.registration_model import RegistrationModel
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_post_v1_account_login():
    mailhog = MailhogApi(host="http://5.63.153.31:5025")
    api = DmApiAccount(host='http://5.63.153.31:5051')
    json_login = LoginCredentialsModel(
        login="user_19",
        password="user_19%",
        rememberMe=True
    )
    json_initial_user = RegistrationModel(
        login="user_19",
        email="user_19@user_19",
        password="user_19%"
    )
    user = api.account.post_v1_account(json=json_initial_user)
    assert user.status_code == 201, f'Expected status code 201, actual status code {user.status_code}'

    token = mailhog.get_token_from_last_email()
    token_response = api.account.put_v1_account_token(
        token=token
    )
    assert token_response.status_code == 200, f'Expected status code 200, ' \
                                              f'actual status code {token_response.status_code}'

    response = api.login.post_v1_account_login(
        json=json_login
    )
    assert response.status_code == 200, f'Expected status code 200, actual status code {response.status_code}'
