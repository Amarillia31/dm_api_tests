import allure
from hamcrest import (
    assert_that,
    has_properties,
)

from dm_api_account.model.rating import Rating
from dm_api_account.model.user_role import UserRole


@allure.suite('Tests for method POST{host}/v1/account')
@allure.sub_suite('Positive test cases')
class TestsPostV1Account:
    @allure.title('Check registration and activation of the new user')
    def test_post_v1_account(
            self,
            facade,
            orm,
            prepare_user,
            assertions
    ):
        """
        Test checks creation, registration and activation of the new user
        """
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        facade.account.register_new_user(login=login, email=email, password=password)
        assertions.check_user_was_created(login=login)

        orm.update_activation_status(login=login, activation_status=True)
        assertions.check_user_war_activated(login=login)
        response = facade.login.login_user(login=login, password=password, _return_http_data_only=True)
        assert_that(
            response.resource, has_properties(
                {
                    "login": login,
                    "roles": [UserRole("Guest"), UserRole("Player")],
                    "rating": Rating(enabled=True, quality=0, quantity=0)
                }
            )
        )

