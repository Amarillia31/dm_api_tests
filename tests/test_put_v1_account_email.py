import requests
from services.dm_api_account import DmApiAccount


def test_put_v1_account_email():
    api = DmApiAccount(host='http://5.63.153.31:5051')
    json = {
        "login": "<string>",
        "password": "<string>",
        "email": "<string>"
    }
    response = api.account.put_v1_account_email(
        json=json
    )
    print(response)
