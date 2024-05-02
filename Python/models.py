from pydantic import BaseModel

class AccountCreate(BaseModel):
    email: str
    password: str

    # Pydantic model for login request body
class Login(BaseModel):
    email: str
    password: str
