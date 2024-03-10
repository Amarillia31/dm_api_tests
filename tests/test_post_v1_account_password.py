import structlog
from hamcrest import (
    assert_that,
    has_entries,
)

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_post_v1_account_password(facade, orm, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    facade.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert_that(
            row, has_entries(
                {
                    'Login': login,
                    'Activated': False
                }
            )
        )

    orm.update_activation_status(login=login, activation_status=True)

    dataset = orm.get_user_by_login(login=login)
    for row in dataset:
        assert_that(row, has_entries(
            {
                'Activated': True
            }
        ))

    token = facade.login.get_auth_token(login=login, password=password)
    facade.account.set_headers(headers=token)
    facade.account.reset_user_password(login=login, email=email, status_code=200)


