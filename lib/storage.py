import json
from datetime import datetime
from typing import Optional

from lib.dto import Token, Entity


class Storage:
    STORAGE_FILE = "/data/storage.json"

    @staticmethod
    def store_token(token: Token):
        try:
            with open(Storage.STORAGE_FILE, "r") as f:
                content = f.read()
                existing_data = json.loads(f.read() if content is not None and content != "" else "{}")
        except FileNotFoundError:
            existing_data = {}

        json_data = {
            "access_token": token.access_token,
            "refresh_token": token.refresh_token,
            "expires_in": token.expires_in,
            "expires_at": token.expires_at.isoformat(),
            "scope": token.scope,
        }

        existing_data["token"] = json_data

        with open(Storage.STORAGE_FILE, "w") as f:
            f.write(json.dumps(existing_data))

    @staticmethod
    def get_token() -> Optional[Token]:
        try:
            with open(Storage.STORAGE_FILE, "r") as f:
                content = f.read()
                existing_data = json.loads(f.read() if content is not None and content != "" else "{}")
        except FileNotFoundError:
            existing_data = {}

        if "token" in existing_data:
            return Token(
                access_token=existing_data["token"]["access_token"],
                refresh_token=existing_data["token"]["refresh_token"],
                expires_in=existing_data["token"]["expires_in"],
                expires_at=datetime.fromisoformat(existing_data["token"]["expires_at"]),
                scope=existing_data["token"]["scope"],
            )

        return None

    @staticmethod
    def store_entities(entities: list[Entity]):
        try:
            with open(Storage.STORAGE_FILE, "r") as f:
                content = f.read()
                existing_data = json.loads(f.read() if content is not None and content != "" else "{}")
        except FileNotFoundError:
            existing_data = {}

        existing_data["entities"] = [{
            "id": entity.id,
            "type": entity.type,
            "name": entity.name,
            "bridge": entity.bridge,
            "home_id": entity.home_id,
            "home_name": entity.home_name,
        } for entity in entities]

        with open(Storage.STORAGE_FILE, "w") as f:
            f.write(json.dumps(existing_data))

    @staticmethod
    def get_entities() -> Optional[list[Entity]]:
        try:
            with open(Storage.STORAGE_FILE, "r") as f:
                content = f.read()
                existing_data = json.loads(f.read() if content is not None and content != "" else "{}")
        except FileNotFoundError:
            existing_data = {}

        if "entities" in existing_data:
            return [Entity(
                id=entity["id"],
                type=entity["type"],
                name=entity["name"],
                bridge=entity["bridge"],
                home_id=entity["home_id"],
                home_name=entity["home_name"],
            ) for entity in existing_data["entities"]]

        return None