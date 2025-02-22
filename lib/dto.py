import dataclasses
from datetime import datetime


@dataclasses.dataclass
class Token:
    access_token: str
    refresh_token: str
    expires_in: int
    expires_at: datetime
    scope: str

    def is_expired(self) -> bool:
        return self.expires_at is not None and datetime.now() > self.expires_at

@dataclasses.dataclass
class Entity:
    id: str
    type: str
    name: str
    bridge: str
    home_id: str
    home_name: str