import structlog

from services.dm_api_account import Facade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_post_v1_account():
    api = Facade(host='http://5.63.153.31:5051')
    login = "user_28"
    password = "user_28%"
    api.account.register_new_user(
        login="user_28",
        email="user_28@user_28",
        password="user_28%"
    )
    api.account.activate_registered_user(login=login)
    api.login.login_user(login=login, password=password)
