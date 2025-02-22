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
                existing_data = json.loads(f.read())
        except FileNotFoundError:
            existing_data = {}

        existing_data["token"] = token.__dict__
        existing_data["token"]["expires_at"] = token.expires_at.isoformat()

        with open(Storage.STORAGE_FILE, "w") as f:
            f.write(json.dumps(existing_data))

    @staticmethod
    def get_token() -> Optional[Token]:
        try:
            with open(Storage.STORAGE_FILE, "r") as f:
                existing_data = json.loads(f.read())
        except FileNotFoundError:
            existing_data = {}

        if "token" in existing_data:
            return Token({
                **existing_data["token"],
                "expires_at": datetime.fromisoformat(existing_data["token"]["expires_at"])
            })

        return None

    @staticmethod
    def store_entities(entities: list[Entity]):
        try:
            with open(Storage.STORAGE_FILE, "r") as f:
                existing_data = json.loads(f.read())
        except FileNotFoundError:
            existing_data = {}

        existing_data["entities"] = [entity.__dict__ for entity in entities]

        with open(Storage.STORAGE_FILE, "w") as f:
            f.write(json.dumps(existing_data))

    @staticmethod
    def get_entities() -> Optional[list[Entity]]:
        try:
            with open(Storage.STORAGE_FILE, "r") as f:
                existing_data = json.loads(f.read())
        except FileNotFoundError:
            existing_data = {}

        if "entities" in existing_data:
            return [Entity(**entity) for entity in existing_data["entities"]]

        return None