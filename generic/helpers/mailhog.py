import json
import pprint
import time

import requests
from requests import session
from requests import Response
from restclient.restclient import Restclient


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

    @decorator
    def get_api_v2_messages(
            self,
            limit: int = 50
    ) -> Response:
        """
        get messages by limit
        :param limit:
        :return:
        """
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
        emails = self.get_api_v2_messages(limit=1).json()
        token_url = json.loads(emails['items'][0]['Content']['Body'])['ConfirmationLinkUrl']
        token = token_url.split('/')[-1]
        return token

    def get_token_by_login(
            self,
            login: str,
            attempt=5
    ):
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


MailhogApi().get_token_by_login(login='user_27')
