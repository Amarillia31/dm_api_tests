from dm_api_account.models import LoginCredentials


class Login:
    def __init__(
            self,
            facade
    ):
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def set_headers(
            self,
            header_name,
            header_value

    ):
        self.facade.login_api.api_client.set_default_header(header_name=header_name, header_value=header_value)

    def login_user(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            _return_http_data_only=False
    ):
        response = self.facade.login_api.v1_account_login_post(
            _return_http_data_only=_return_http_data_only,
            login_credentials=LoginCredentials(
                login=login,
                password=password,
                remember_me=remember_me
            )
        )
        return response

    def get_auth_token(
            self,
            login: str,
            password: str
    ):
        response = self.login_user(
            login=login,
            password=password
        )
        token = response[2]['X-Dm-Auth-Token']
        return token

    def logout_user(
            self,
            status_code: int = 204,
            **kwargs
    ):
        response = self.facade.login_api.v1_account_login_delete(status_code=status_code, **kwargs)
        return response

    def logout_user_from_all_devices(
            self,
            status_code: int = 204,
            **kwargs
    ):
        response = self.facade.login_api.v1_account_login_all_delete(status_code=status_code, **kwargs)
        return response
