import allure
import pytest
from hamcrest import (
    assert_that,
    has_entries,
)

from generic.assertions.response_checker import check_status_code_http
from utilites import random_string


@pytest.mark.parametrize(
    'login, email, password, status_code, check', [
        ('12', '12@12.ru', '123456', 201, ''),
        ('12', '12@12.ru', random_string(1, 5), 400, {"Password": ["Short"]}),
        ('1', '12@12.ru', '123456', 400, {"Login": ["Short"]}),
        ('12', '12@', '123456', 400, {"Email": ["Invalid"]}),
        ('12', '12', '123456', 400, {"Email": ["Invalid"]})
    ]
)
@allure.title('Check user login')
def test_create_and_activated_user_with_random_params(
        facade,
        orm,
        login,
        email,
        password,
        status_code,
        check,
        assertions
):

    orm.delete_user_by_login(login=login)
#    facade.mailhog.delete_all_messages()
    with check_status_code_http(expected_status_code=status_code, expected_result=check):
        response = facade.account.register_new_user(login=login, email=email, password=password)
    if status_code == 201:
        assertions.check_user_was_created(login=login)
        facade.account.activate_registered_user(login=login)
        assertions.check_user_war_activated(login=login)
        facade.login.login_user(login=login, password=password)
