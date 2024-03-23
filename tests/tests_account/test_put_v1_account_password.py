import allure
import structlog
from hamcrest import (
    assert_that,
    has_properties,
)

from apis.dm_api_account.models.user_envelope_model import (
    UserRole,
    Rating,
)

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@allure.suite('Tests for method PUT{host}/v1/account/password')
@allure.sub_suite('Positive test cases')
class TestsPutV1AccountPassword:
    @allure.title('Change registered user password')
    def test_put_v1_account_password(self, facade, orm, prepare_user, assertions):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        new_password = prepare_user.new_password

        facade.account.register_new_user(login=login, email=email, password=password)
        assertions.check_user_was_created(login=login)

        orm.update_activation_status(login=login, activation_status=True)
        assertions.check_user_war_activated(login=login)

        token = facade.login.get_auth_token(login=login, password=password)
        facade.account.set_headers(headers=token)
        facade.account.reset_user_password(login=login, email=email, status_code=200)
        response = facade.account.change_user_password(login=login, old_password=password, new_password=new_password)

        assert_that(
            response.resource, has_properties(
                {
                    "login": login,
                    "roles": [UserRole.guest, UserRole.player],
                    "rating": Rating(enabled=True, quality=0, quantity=0)
                }
            )
        )
