import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi

import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_put_v1_account_token():
    mailhog = MailhogApi(host="http://5.63.153.31:5025")
    api = DmApiAccount(host='http://5.63.153.31:5051')
    json = {
        "login": "user_10",
        "email": "user_10@user_10",
        "password": "user_10%"
    }
    user = api.account.post_v1_account(json=json)
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(
        token=token
    )
    assert response.status_code == 200, f'Expected status code 200, actual status code {response.status_code}'

