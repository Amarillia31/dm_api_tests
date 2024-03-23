from collections import namedtuple

import allure
import pytest
import structlog
from vyper import v
from pathlib import Path

from generic.assertions.post_v1_account import AssertionsPostV1Account
from generic.helpers.dm_db import DmDatabase
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
from generic.helpers.mailhog import MailhogApi
from data.post_v1_account import PostV1AccountData as user_data


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


@pytest.fixture
def mailhog():
    return MailhogApi(host=v.get('service.mailhog'))


@pytest.fixture
def facade(
        mailhog,
        request
):
    return Facade(
        host=v.get('service.dm_api_account'),
        mailhog=mailhog
    )


connect = None


@pytest.fixture
def db():
    global connect
    if connect is None:
        connect = DmDatabase(
            user=v.get('database.dm3_5.user'),
            password=v.get('database.dm3_5.password'),
            host=v.get('database.dm3_5.host'),
            database=v.get('database.dm3_5.database')
        )
    return connect


@pytest.fixture
def orm():
    orm = OrmDatabase(
        user=v.get('database.dm3_5.user'),
        password=v.get('database.dm3_5.password'),
        host=v.get('database.dm3_5.host'),
        database=v.get('database.dm3_5.database')
    )
    yield orm
    orm.db.close_connection()


@pytest.fixture
def assertions(db):
    return AssertionsPostV1Account(db)


@allure.step('Подготовка нового пользователя')
@pytest.fixture
def prepare_user(
        facade,
        orm
):
    user = namedtuple('User', 'login, email, password, new_password, new_email')
    User = user(
        login=user_data.login, email=user_data.email, password=user_data.password, new_password=user_data.new_password,
        new_email=user_data.new_email
    )
    orm.delete_user_by_login(login=User.login)
    dataset = orm.get_user_by_login(login=User.login)
    assert len(dataset) == 0
    #    facade.mailhog.delete_all_messages()
    return User


options = (
    'service.dm_api_account',
    'service.mailhog',
    'database.dm3_5.host'
)


@pytest.fixture(autouse=True)
def set_config(
        request
):
    config = Path(__file__).parents[2].joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.set_config_type("yaml")
    v.read_in_config()
    for option in options:
        v.set(option, request.config.getoption(f'--{option}'))


def pytest_addoption(
        parser
):
    parser.addoption('--env', action='store', default='stg')
    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)
