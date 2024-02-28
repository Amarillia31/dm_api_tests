import structlog

from services.dm_api_account import Facade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_delete_v1_account_login_all():
    api = Facade(host='http://5.63.153.31:5051')
    login = "user_35"
    password = "user_35%"
    api.account.register_new_user(
        login="user_35",
        email="user_35@user_35",
        password="user_35%"
    )
    api.account.activate_registered_user(login=login)

    token = api.login.get_auth_token(login=login, password=password)
    api.login.set_headers(headers=token)
    api.login.logout_user_from_all_devices()
