import allure
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


@allure.suite('Tests for method PUT{host}/v1/account/token')
@allure.sub_suite('Positive test cases')
class TestsPutV1AccountEmail:
    @allure.title('Activate User')
    def test_put_v1_account_token(self, facade, orm, prepare_user, assertions):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        facade.account.register_new_user(login=login, email=email, password=password)
        assertions.check_user_was_created(login=login)

        response = facade.account.activate_registered_user(login=login)
        assertions.check_user_war_activated(login=login)

        assert_that(response.resource, has_properties({
            "login": login,
            "roles": [UserRole.guest, UserRole.player],
            "rating": Rating(enabled=True, quality=0, quantity=0)
        }))
