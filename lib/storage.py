import json
from typing import Optional

from lib.dto import Token, Entity


class Storage:
    STORAGE_FILE = "/data/storage.json"

    @staticmethod
    def store_token(token: Token):
        with open(Storage.STORAGE_FILE, "r") as f:
            existing_data = json.loads(f.read())

        existing_data["token"] = token.__dict__

        with open(Storage.STORAGE_FILE, "w") as f:
            f.write(json.dumps(existing_data))

    @staticmethod
    def get_token() -> Optional[Token]:
        with open(Storage.STORAGE_FILE, "r") as f:
            existing_data = json.loads(f.read())

        if "token" in existing_data:
            return Token(**existing_data["token"])

        return None

    @staticmethod
    def store_entities(entities: list[Entity]):
        with open(Storage.STORAGE_FILE, "r") as f:
            existing_data = json.loads(f.read())

        existing_data["entities"] = [entity.__dict__ for entity in entities]

        with open(Storage.STORAGE_FILE, "w") as f:
            f.write(json.dumps(existing_data))

    @staticmethod
    def get_entities() -> Optional[list[Entity]]:
        with open(Storage.STORAGE_FILE, "r") as f:
            existing_data = json.loads(f.read())

        if "entities" in existing_data:
            return [Entity(**entity) for entity in existing_data["entities"]]

        return None