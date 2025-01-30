from datetime import datetime
from typing import Optional

from bson import ObjectId
from typing_extensions import Annotated
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]
UserConfig = {"populate_by_name": True, "json_encoders": {ObjectId: str}}


class BlacklistedToken(BaseModel):
    model_config = ConfigDict(**UserConfig)

    token: str
    user_id: PyObjectId
    expires_at: Optional[datetime] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)


class LoginRequest(BaseModel):
    username: str
    password: str
    remember_me: Optional[bool] = False
