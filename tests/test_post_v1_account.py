import requests
from services.dm_api_account import DmApiAccount


def test_post_v1_account():
    api = DmApiAccount(host='http://5.63.153.31:5051')
    json = {
        "login": "user_05",
        "email": "user_05@user_05",
        "password": "user_05%"
    }
    response = api.account.post_v1_account(
        json=json
    )
    print(response)
