import json
import time

import allure
from requests import Response
from common_libs.restclient.restclient import Restclient


def decorator(
        fn
):
    def wrapper(
            *args,
            **kwargs
    ):

        for i in range(5):
            response = fn(*args, **kwargs)
            emails = response.json()['items']

            if len(emails) < 5:
                time.sleep(2)
                continue
            else:
                return response

    return wrapper


class MailhogApi:
    def __init__(
            self,
            host="http://5.63.153.31:5025"
    ):
        self.host = host
        self.client = Restclient(host=host)

#    @decorator
    def get_api_v2_messages(
            self,
            limit: int = 50
    ) -> Response:
        """
        get messages by limit
        :param limit:
        :return:
        """
        with allure.step('Check emails at web gui'):
            response = self.client.get(
                path=f"/api/v2/messages",
                params={
                    'limit': limit
                }
            )
        return response

    def get_token_from_last_email(
            self
    ) -> str:
        """
        get user activation token from last email
        :return:
        """
        with allure.step('Get token from last email'):
            emails = self.get_api_v2_messages(limit=1).json()
            token_url = json.loads(emails['items'][0]['Content']['Body'])['ConfirmationLinkUrl']
            token = token_url.split('/')[-1]
        return token

    def get_token_by_login(
            self,
            login: str,
            attempt=5
    ):
        with allure.step('Get token from email by login name to activate user'):
            if attempt == 0:
                raise AssertionError(f'Email with login {login} was not found')
            emails = self.get_api_v2_messages(limit=100).json()['items']
            for email in emails:
                user_data = json.loads(email['Content']['Body'])
                if login == user_data.get('Login'):
                    token = user_data.get('ConfirmationLinkUrl').split('/')[-1]
                    print(token)
                    return token
                time.sleep(2)
        return self.get_token_by_login(login=login, attempt=attempt - 1)

    def get_token_for_reset_password(
            self,
            login: str,
            attempt=5
    ):
        with allure.step('Get token from email by login name to reset password'):
            if attempt == 0:
                raise AssertionError(f'Email with login {login} was not found')
            emails = self.get_api_v2_messages(limit=100).json()['items']
            for email in emails:
                user_data = json.loads(email['Content']['Body'])
                if login == user_data.get('Login'):
                    token = user_data.get('ConfirmationLinkUri').split('/')[-1]
                    print(token)
                    return token
                time.sleep(2)
        return self.get_token_by_login(login=login, attempt=attempt - 1)

    def delete_all_messages(
            self
    ):
        with allure.step('Delete all emails'):
            response = self.client.delete(path='/api/v1/messages')
        return response


# TODO УДАЛИТЬ ПОПОЗЖЕ
# response = MailhogApi().get_token_by_login(login='user_60')
# # response = MailhogApi().get_api_v2_messages()
# print(response)
#
