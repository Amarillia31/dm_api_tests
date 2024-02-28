import structlog

from services.dm_api_account import Facade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_post_v1_account_password():
    api = Facade(host='http://5.63.153.31:5051')

    login = "user_39"
    password = "user_39%"
    email = "user_39@user_39"
    api.account.register_new_user(
        login="user_39",
        email="user_39@user_39",
        password="user_39%"
    )
    api.account.activate_registered_user(login=login)

    token = api.login.get_auth_token(login=login, password=password)
    api.account.set_headers(headers=token)
    api.account.reset_user_password(login=login, email=email)
