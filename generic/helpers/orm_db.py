from typing import List

import allure
from sqlalchemy import (
    select,
    delete,
    update,
)

from generic.helpers.orm_models import User
from common_libs.orm_client.orm_client import OrmClient


class OrmDatabase:

    def __init__(self, user, password, host, database):
        self.db = OrmClient(user, password, host, database)

    def get_all_users(self):
        query = select(User)
        dataset = self.db.send_query(query=query)
        return dataset

    def get_user_by_login(self, login: str) -> List[User]:
        query = select(User).where(
            User.Login == login
        )
        dataset = self.db.send_query(query=query)
        return dataset

    def delete_user_by_login(self, login: str):
        with allure.step('Check user was removed'):
            query = delete(User).where(
                User.Login == login
            )
            dataset = self.db.send_bulk_query(query=query)
        return dataset

    def update_activation_status(self, login: str, activation_status: bool):
        with allure.step('User activation'):
            query = update(User).where(
                User.Login == login
            ).values(Activated=activation_status)
            dataset = self.db.send_bulk_query(query=query)
        return dataset
