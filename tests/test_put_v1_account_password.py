from dm_api_account.models.change_password_model import ChangePasswordModel
from services.dm_api_account import DmApiAccount


def test_put_v1_account_password():
    api = DmApiAccount(host='http://5.63.153.31:5051')
    json = ChangePasswordModel(
        login="<string>",
        token="<uuid>",
        oldPassword="<string>",
        newPassword="<string>"
    )

    response = api.account.put_v1_account_password(
        json=json
    )
    print(response)
