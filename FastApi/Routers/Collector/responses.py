from pydantic import BaseModel


class Party(BaseModel):
    id: str
    home_phone: str
    mobile_phone: str
    phone: str


class Intake(BaseModel):
    id: str
    status: str
