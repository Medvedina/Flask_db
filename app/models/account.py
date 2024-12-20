from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator, model_validator
from typing_extensions import Self

class RegistrateDTO(BaseModel):
    id: int = Field(default=None)
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=30)
    password_confirm: str = Field(min_length=6, max_length=30)
    full_name: str = Field(min_length=3, max_length=50)
    birth_date: str = Field(default=None)
    role: str = Field(default='User')
        
    @field_validator('birth_date', mode='before')
    def validate_birth_date(cls, value):
    
        today = date.today()
        print(today)
        birth_date=datetime.strptime(value, '%d.%m.%Y').date()
        print(birth_date)

        if birth_date <= today:
            return value
        else:
            raise ValueError(f"Дата рождения должна быть не позже {today}")
    
    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password_confirm != self.password:
            raise ValueError('Пароли не совпадают')
        else:
            return self