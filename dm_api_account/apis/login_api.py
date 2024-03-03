from requests import Response
from utilites import validate_request_json, validate_status_code
from restclient.restclient import Restclient
from ..models import *
from ..models import UserEnvelope


class LoginApi:
    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.client = Restclient(host=host, headers=headers)
        self.client.session.headers.update(headers) if headers else None

    def post_v1_account_login(
            self,
            json: LoginCredentials,
            status_code: int = 200,
            full_response: bool = True,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        :param full_response:
        :param status_code: server response status
        :param json login_credentials_model
        Authenticate via credentials
        :return:
        """

        response = self.client.post(
            path=f"/v1/account/login",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)
        if response.status_code == 200:
            UserEnvelope(**response.json())

        if full_response is True:
            return response
        else:
            return UserEnvelope(**response.json())

    def delete_v1_account_login(
            self,
            status_code: int = 204,
            **kwargs
    ):
        """
        Logout as current user
        :return:
        """

        response = self.client.delete(
            path=f"/v1/account/login",
            **kwargs
        )
        validate_status_code(response, status_code)
        return response

    def delete_v1_account_login_all(
            self,
            status_code: int = 204,
            **kwargs
    ):
        """
        Logout from every device
        :return:
        """

        response = self.client.delete(
            path=f"/v1/account/login/all",
            **kwargs
        )
        validate_status_code(response, status_code)
        return response
