import structlog

from dm_api_account.models.change_email_model import ChangeEmailModel
from dm_api_account.models.registration_model import RegistrationModel
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_put_v1_account_email():
    api = DmApiAccount(host='http://5.63.153.31:5051')
    mailhog = MailhogApi(host="http://5.63.153.31:5025")
    json_replace = ChangeEmailModel(
        login="user_20",
        password="user_20%",
        email="user_20_rpl@user_20"
    )
    json_initial_user = RegistrationModel(
        login="user_20",
        email="user_20@user_20",
        password="user_20%"
    )
    user = api.account.post_v1_account(json=json_initial_user)
    assert user.status_code == 201, f'Expected status code 201, actual status code {user.status_code}'

    token = mailhog.get_token_from_last_email()
    token_response = api.account.put_v1_account_token(
        token=token
    )
    assert token_response.status_code == 200, f'Expected status code 200, ' \
                                              f'actual status code {token_response.status_code}'

    response = api.account.put_v1_account_email(
        json=json_replace
    )
    assert response.status_code == 200, f'Expected status code 200, actual status code {response.status_code}'

