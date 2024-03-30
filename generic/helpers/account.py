from dm_api_account.model.change_password import ChangePassword
from dm_api_account.models import (
    Registration,
    ResetPassword,
    ChangeEmail,
)


class Account:
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

    def register_new_user(
            self,
            login: str,
            email: str,
            password: str,
            **kwargs
    ):
        response = self.facade.account_api.register(
            registration=Registration(
                login=login,
                email=email,
                password=password
            ),
            **kwargs
        )
        return response

    def activate_registered_user(
            self,
            login: str,
            **kwargs
    ):
        token = self.facade.mailhog.get_token_by_login(login=login)
        response = self.facade.account_api.activate(token=token, **kwargs)
        return response

    def get_current_user_info(
            self,
            **kwargs
    ):
        response = self.facade.account_api.get_current(**kwargs)
        return response

    def reset_user_password(
            self,
            login: str,
            email: str,
            **kwargs
    ):
        response = self.facade.account_api.reset_password(
            reset_password=ResetPassword(
                login=login,
                email=email
            ),
            **kwargs
        )
        return response

    def change_user_password(
            self,
            login: str,
            old_password: str,
            new_password: str,
            **kwargs
    ):
        token = self.facade.mailhog.get_token_for_reset_password(login=login)

        response = self.facade.account_api.change_password(
            change_password=ChangePassword(
                login=login,
                token=token,
                old_password=old_password,
                new_password=new_password
            ),
            **kwargs
        )
        return response

    def change_registered_user_email(
            self,
            login: str,
            password: str,
            email: str,
            status_code: int = 200,
            **kwargs
    ):
        response = self.facade.account_api.put_v1_account_email(
            json=ChangeEmail(
                login=login,
                password=password,
                email=email
            ),
            status_code=status_code,
            **kwargs
        )
        return response
