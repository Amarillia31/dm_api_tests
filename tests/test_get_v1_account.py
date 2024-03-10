import structlog
from hamcrest import (
    assert_that,
    has_properties,
    has_entries,
)

from dm_api_account.models.user_envelope_model import (
    UserRole,
    Rating,
)

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


def test_get_v1_account(facade, orm, prepare_user):
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
    facade.login.set_headers(headers=token)
    response = facade.account.get_current_user_info()
    assert_that(
        response.resource, has_properties(
            {
                "login": login,
                "roles": [UserRole.guest, UserRole.player],
                "rating": Rating(enabled=True, quality=0, quantity=0)
            }
        )
    )
