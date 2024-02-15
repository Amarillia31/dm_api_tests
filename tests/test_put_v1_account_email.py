import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_put_v1_account_email():
    api = DmApiAccount(host='http://5.63.153.31:5051')
    mailhog = MailhogApi(host="http://5.63.153.31:5025")
    json_replace = {
        "login": "user_11",
        "password": "user_11%",
        "email": "user_11_rpl@user_11"
    }
    json_initial_user = {
        "login": "user_11",
        "email": "user_11@user_11",
        "password": "user_11%"
    }
    user = api.account.post_v1_account(json=json_initial_user)
    token = mailhog.get_token_from_last_email()
    token_response = api.account.put_v1_account_token(
        token=token
    )
    response = api.account.put_v1_account_email(
        json=json_replace
    )
    assert response.status_code == 200, f'Expected status code 200, actual status code {response.status_code}'

