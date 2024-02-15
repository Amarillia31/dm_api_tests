import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_post_v1_account_login():
    mailhog = MailhogApi(host="http://5.63.153.31:5025")
    api = DmApiAccount(host='http://5.63.153.31:5051')
    json_login = {
        "login": "user_15",
        "password": "user_15%",
        "rememberMe": True
    }
    json_initial_user = {
        "login": "user_15",
        "email": "user_15@user_15",
        "password": "user_15%"
    }
    user = api.account.post_v1_account(json=json_initial_user)
    token = mailhog.get_token_from_last_email()
    token_response = api.account.put_v1_account_token(
        token=token
    )
    response = api.login.post_v1_account_login(
        json=json_login
    )
    assert response.status_code == 200, f'Expected status code 200, actual status code {response.status_code}'
