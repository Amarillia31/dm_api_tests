import json
import pprint

import requests
from requests import session
from requests import Response
from restclient.restclient import Restclient


class MailhogApi:
    def __init__(self, host="http://5.63.153.31:5025"):
        self.host = host
        self.client = Restclient(host=host)

    def get_api_v2_messages(self, limit: int = 50) -> Response:
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

    def get_token_from_last_email(self) -> str:
        """
        get user activation token from last email
        :return:
        """
        emails = self.get_api_v2_messages(limit=1).json()
        token_url = json.loads(emails['items'][0]['Content']['Body'])['ConfirmationLinkUrl']
        token = token_url.split('/')[-1]
        return token
