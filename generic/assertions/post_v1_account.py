import allure
from hamcrest import (
    assert_that,
    has_entries,
)

from generic.helpers.orm_db import OrmDatabase


class AssertionsPostV1Account:

    def __init__(self, db: OrmDatabase):
        self.db = db

    def check_user_was_created(
            self,
            login: str
    ):
        with allure.step('Check user is created'):
            dataset = self.db.get_user_by_login(login=login)
            for row in dataset:
                assert_that(
                    row, has_entries(
                        {
                            'Login': login,
                            'Activated': False
                        }
                    )
                )

    def check_user_war_activated(
            self,
            login: str
    ):
        with allure.step('Check user is activated'):
            dataset = self.db.get_user_by_login(login=login)
            for row in dataset:
                assert_that(
                    row, has_entries(
                        {
                            'Activated': True
                        }
                    )
                )

    def check_email_was_changed(
            self,
            login: str,
            email: str
    ):
        with allure.step('Check email changed'):
            dataset = self.db.get_user_by_login(login=login)
            for row in dataset:
                assert_that(
                    row, has_entries(
                        {
                            'Email': email
                        }
                    )
                )