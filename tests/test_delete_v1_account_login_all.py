import structlog

from services.dm_api_account import DmApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_delete_v1_account_login_all():
    api = DmApiAccount(host='http://5.63.153.31:5051')
    response = api.login.delete_v1_account_login_all()
    print(response)
