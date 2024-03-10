from collections import namedtuple

import pytest
import structlog
from generic.helpers.dm_db import DmDatabase
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade
from generic.helpers.mailhog import MailhogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


@pytest.fixture
def mailhog():
    return MailhogApi(host='http://5.63.153.31:5025')


@pytest.fixture
def facade(
        mailhog
):
    return Facade(host='http://5.63.153.31:5051', mailhog=mailhog)


@pytest.fixture
def db():
    db = DmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')
    return db


@pytest.fixture
def orm():
    orm = OrmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')
    yield orm
    orm.db.close_connection()


@pytest.fixture
def prepare_user(
        facade,
        orm
):
    user = namedtuple('User', 'login, email, password, new_password, new_email')
    User = user(
        login="user_60", email="user_60@user_60", password="user_60%", new_password="user_60%!",
        new_email="user_60_upd@user_60"
    )
    orm.delete_user_by_login(login=User.login)
    dataset = orm.get_user_by_login(login=User.login)
    assert len(dataset) == 0
    #    facade.mailhog.delete_all_messages()
    return User
