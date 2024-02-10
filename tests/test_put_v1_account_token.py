import requests
from services.dm_api_account import DmApiAccount


def test_post_v1_account_token():
    api = DmApiAccount(host='http://5.63.153.31:5051')
    token = '07bdc21e-5c9d-40f6-b364-1d5ddbc01bfa'
    response = api.account.put_v1_account_token(
        token=token
    )
    print(response)

