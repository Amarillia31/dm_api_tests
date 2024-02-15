import requests
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_post_v1_account():
    mailhog = MailhogApi(host="http://5.63.153.31:5025")
    api = DmApiAccount(host='http://5.63.153.31:5051')
    json = {
        "login": "user_08",
        "email": "user_08@user_08",
        "password": "user_08%"
    }
    response = api.account.post_v1_account(json=json)
    assert response.status_code == 201, f'Expected status code 201, actual status code {response.status_code}'
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token)

