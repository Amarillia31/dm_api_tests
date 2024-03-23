import structlog
import allure
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
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


@allure.suite('Tests for method GET{host}/v1/account')
@allure.sub_suite('Positive test cases')
class TestsGetV1Account:
    @allure.title('Check registration, activation and receiving  info of the new user')
    def test_get_v1_account(self, facade, orm, prepare_user, assertions):
        """
        Test checks getting user info
        """
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        facade.account.register_new_user(login=login, email=email, password=password)
        assertions.check_user_was_created(login=login)

        orm.update_activation_status(login=login, activation_status=True)
        assertions.check_user_war_activated(login=login)

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
