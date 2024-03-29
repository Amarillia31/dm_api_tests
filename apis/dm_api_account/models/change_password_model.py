from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    Extra,
    Field,
    StrictStr,
    validator,
    field_validator,
)


class ChangePassword(BaseModel):
    class Config:
        extra = Extra.forbid

    login: Optional[StrictStr] = Field(None, description='User login')
    token: Optional[UUID] = Field(None, description='Password reset token')
    old_password: Optional[StrictStr] = Field(
        None, alias='oldPassword', description='Old password'
    )
    new_password: Optional[StrictStr] = Field(
        None, alias='newPassword', description='New password'
    )

