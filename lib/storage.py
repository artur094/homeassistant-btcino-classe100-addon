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
                existing_data = json.loads(content if content is not None and content != "" else "{}")
        except FileNotFoundError:
            existing_data = {}

        existing_data["token"] = token.to_json()

        with open(Storage.STORAGE_FILE, "w") as f:
            f.write(json.dumps(existing_data))

    @staticmethod
    def get_token() -> Optional[Token]:
        try:
            with open(Storage.STORAGE_FILE, "r") as f:
                content = f.read()
                existing_data = json.loads(content if content is not None and content != "" else "{}")
        except FileNotFoundError:
            existing_data = {}

        if "token" in existing_data:
            return Token.from_json(existing_data["token"])

        return None

    @staticmethod
    def store_entities(entities: list[Entity]):
        try:
            with open(Storage.STORAGE_FILE, "r") as f:
                content = f.read()
                existing_data = json.loads(content if content is not None and content != "" else "{}")
        except FileNotFoundError:
            existing_data = {}

        existing_data["entities"] = [entity.to_json() for entity in entities]

        with open(Storage.STORAGE_FILE, "w") as f:
            f.write(json.dumps(existing_data))

    @staticmethod
    def get_entities() -> Optional[list[Entity]]:
        try:
            with open(Storage.STORAGE_FILE, "r") as f:
                content = f.read()
                existing_data = json.loads(content if content is not None and content != "" else "{}")
        except FileNotFoundError:
            existing_data = {}

        if "entities" in existing_data:
            return [Entity.from_json(entity) for entity in existing_data["entities"]]

        return None