import json
from typing import Optional

from lib.dto import Token, Entity


class Storage:
    @staticmethod
    def store_token(token: Token, storage_file: str):
        with open(storage_file, "r") as f:
            existing_data = json.loads(f.read())

        existing_data["token"] = token.__dict__

        with open(storage_file, "w") as f:
            f.write(json.dumps(existing_data))

    @staticmethod
    def get_token(storage_file: str) -> Optional[Token]:
        with open(storage_file, "r") as f:
            existing_data = json.loads(f.read())

        if "token" in existing_data:
            return Token(**existing_data["token"])

        return None

    @staticmethod
    def store_entities(entities: list[Entity], storage_file: str):
        with open(storage_file, "r") as f:
            existing_data = json.loads(f.read())

        existing_data["entities"] = [entity.__dict__ for entity in entities]

        with open(storage_file, "w") as f:
            f.write(json.dumps(existing_data))

    @staticmethod
    def get_entities(storage_file: str) -> Optional[list[Entity]]:
        with open(storage_file, "r") as f:
            existing_data = json.loads(f.read())

        if "entities" in existing_data:
            return [Entity(**entity) for entity in existing_data["entities"]]

        return None