import uuid

import allure
import records
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)]
)


class DbClient:
    def __init__(
            self,
            user,
            password,
            host,
            database,
            isolation_level='AUTOCOMMIT'
    ):
        connection_string = f'postgresql://{user}:{password}@{host}/{database}'
        self.db = records.Database(connection_string, isolation_level=isolation_level)
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='db')

    def send_query(
            self,
            query
    ):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=query
        )
        allure.attach(
            query,
            name='DB query',
            attachment_type=allure.attachment_type.TEXT
        )
        dataset = self.db.query(query=query).as_dict()
        log.msg(
            event='response',
            dataset=dataset
        )
        allure.attach(
            str(dataset),
            name='DB response',
            attachment_type=allure.attachment_type.TEXT
        )
        return dataset

    def send_bulk_query(
            self,
            query
    ):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query='query'
        )
        allure.attach(
            query,
            name='DB query',
            attachment_type=allure.attachment_type.TEXT
        )
        self.db.bulk_query(query=query)

# TODO
# if __name__=="__main__":
#     db = DbClient(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')
#     query = 'select * from "public"."Users"'
#     db.send_query(query)
