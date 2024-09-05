from pydantic import BaseModel, Field

class UserRegisterSchema(BaseModel):
    full_name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    

class UserLogin(BaseModel):
    email : str = Field(...)
    password : str = Field(...)

    