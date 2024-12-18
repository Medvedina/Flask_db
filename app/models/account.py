from dataclasses import dataclass


@dataclass
class Account:
    
    id: int
    login: str
    firstname: str
    lastname: str
