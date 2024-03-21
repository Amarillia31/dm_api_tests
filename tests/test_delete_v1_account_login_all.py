import allure
import structlog
from hamcrest import (
    assert_that,
    has_entries,
)

from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


@allure.suite('Tests for method DELETE{host}/v1/account/login/all')
@allure.sub_suite('Positive test cases')
class TestsDeleteV1AccountLoginAll:
    @allure.title('Logout all users')
    def test_delete_v1_account_login_all(self, facade, orm, prepare_user, assertions):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        facade.account.register_new_user(login=login, email=email, password=password)
        assertions.check_user_was_created(login=login)

        orm.update_activation_status(login=login, activation_status=True)
        assertions.check_user_war_activated(login=login)

        token = facade.login.get_auth_token(login=login, password=password)
        facade.login.set_headers(headers=token)
        facade.login.logout_user_from_all_devices()
