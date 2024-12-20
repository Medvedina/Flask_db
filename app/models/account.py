from datetime import date, datetime
from pydantic import BaseModel, Field, validator


class Account(BaseModel):
    id: int = Field(default=None)
    login: str
    password: str = Field(min_length=6, max_length=30)
    full_name: str
    birth_date: str = Field(default=None)
    role: str = Field(default='User')

    
    @validator('birth_date', pre=True)
    def validate_birth_date(cls, value):
        today = date.today()
        print(today)
        birth_date=datetime.strptime(value, '%d.%m.%Y').date()
        print(birth_date)

        if birth_date <= today:
            return value
        else:
            raise ValueError(f"Дата рождения должна быть не позже {today}")