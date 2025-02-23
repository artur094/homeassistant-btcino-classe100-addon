import dataclasses
from datetime import datetime
from typing import Optional


@dataclasses.dataclass
class Token:
    access_token: str
    refresh_token: str
    expires_in: int
    expires_at: datetime
    scope: str

    def is_expired(self) -> bool:
        return self.expires_at is not None and datetime.now() > self.expires_at

    def to_json(self):
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "expires_at": self.expires_at.isoformat(),
            "scope": self.scope,
        }

    @staticmethod
    def from_json(json):
        return Token(
            access_token=json["access_token"],
            refresh_token=json["refresh_token"],
            expires_in=json["expires_in"],
            expires_at=datetime.fromisoformat(json["expires_at"]),
            scope=json["scope"],
        )

@dataclasses.dataclass
class User:
    username: str
    password: str
    client_secret: str

    def to_json(self):
        return {
            "username": self.username,
            "password": self.password,
            "client_secret": self.client_secret,
        }

    @staticmethod
    def from_json(json):
        return User(
            username=json["username"],
            password=json["password"],
            client_secret=json["client_secret"],
        )

@dataclasses.dataclass
class Entity:
    id: str
    type: str
    name: str
    bridge: str
    home_id: str
    home_name: str

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "bridge": self.bridge,
            "home_id": self.home_id,
            "home_name": self.home_name,
        }

    @staticmethod
    def from_json(json):
        return Entity(
            id=json["id"],
            type=json["type"],
            name=json["name"],
            bridge=json["bridge"],
            home_id=json["home_id"],
            home_name=json["home_name"],
        )