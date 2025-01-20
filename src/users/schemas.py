from datetime import datetime

from bson import ObjectId
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic.functional_validators import BeforeValidator

from .enums import UserRoles

PyObjectId = Annotated[str, BeforeValidator(str)]
UserConfig = {"populate_by_name": True, "json_encoders": {ObjectId: str}}


class UserBase(BaseModel):
    model_config = ConfigDict(**UserConfig)

    email: EmailStr
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    role: UserRoles
    date_of_birth: Optional[datetime] = Field(default=None)
    phone: Optional[int] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)


class UserOut(UserBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
