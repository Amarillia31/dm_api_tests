from pydantic import field_validator

from apis.dm_api_account.models.change_password_model import ChangePassword


class CustomChangePassword(ChangePassword):
    ...

    @field_validator('token')
    def uuid_as_str(v):
        return str(v)
