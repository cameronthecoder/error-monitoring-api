from datetime import datetime
from databases import Database
from dataclasses import dataclass, asdict

@dataclass
class User:
    id: int
    email: str
    password_hash: str
    created: datetime