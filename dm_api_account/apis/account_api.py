from requests import Response
from utilites import (
    validate_request_json,
    validate_status_code,
)

from ..models import *
from restclient.restclient import Restclient


class AccountApi:
    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.client = Restclient(host=host, headers=headers)
        self.client.session.headers.update(headers) if headers else None

    def post_v1_account(
            self,
            json: Registration,
            status_code: int = 201,
            **kwargs
    ) -> Response:
        """
        :param status_code: server response status
        :param json registration_model
        Register new user
        :return:
        """

        response = self.client.post(
            path=f"/v1/account",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)
        return response

    def post_v1_account_password(
            self,
            json: ResetPassword,
            status_code: int = 201,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        :param status_code: server response status
        :param json reset_password_model
        Reset registered user password
        :return:
        """

        response = self.client.post(
            path=f"/v1/account/password",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)
        if response.status_code == 201:
            UserEnvelope(**response.json())
        return response

    def put_v1_account_email(
            self,
            json: ChangeEmail,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        :param status_code: server response status
        :param json ChangeEmailModel
        Change registered user email
        :return:
        """

        response = self.client.put(
            path=f"/v1/account/email",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)
        if response.status_code == 200:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_password(
            self,
            json: ChangePassword,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        :param status_code: server response status
        :param json ChangePasswordModel
        Change registered user password
        :return:
        """

        response = self.client.put(
            path=f"/v1/account/password",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)
        if response.status_code == 200:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_token(
            self,
            token,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        Activate registered user
        :return:
        """

        response = self.client.put(
            path=f"/v1/account/{token}",
            **kwargs
        )
        validate_status_code(response, status_code)
        if response.status_code == 200:
            return UserEnvelope(**response.json())
        return response

    def get_v1_account(
            self,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserDetailsEnvelope:
        """
        Get current user
        :return:
        """

        response = self.client.get(
            path=f"/v1/account",
            **kwargs
        )
        validate_status_code(response, status_code)
        if response.status_code == 200:
            UserDetailsEnvelope(**response.json())
        return response
