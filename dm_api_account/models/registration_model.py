from pydantic import BaseModel, StrictStr, Field
from enum import Enum
from typing import List


class RegistrationModel(BaseModel):
    login: StrictStr
    email: StrictStr
    password: StrictStr
