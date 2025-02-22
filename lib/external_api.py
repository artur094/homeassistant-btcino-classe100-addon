import datetime
from typing import Optional

import requests

from lib.dto import Token, Entity
from lib.exceptions import ExternalApiException


class ExternalApi:
    HOST = "https://app.netatmo.net/syncapi/v1"

    @staticmethod
    def login(username: str, password: str, client_secret: str, token: Optional[Token]) -> Token:
        data = {
            "app.version": "4.1.1.3",
            "grant_type": "password",
            "scope": "security_scopes",
            "client_secret": client_secret,
            "client_id": "na_client_android_welcome",
            "username": username,
            "password": password,
        }

        if token is not None:
            data["refresh_token"] = token.refresh_token

        response = requests.post(f"{ExternalApi.HOST}/oauth2/token", files=data)

        if response.status_code > 299:
            raise ExternalApiException("Login failed")

        response_json = response.json()

        return Token(
            access_token=response_json.get("access_token"),
            refresh_token=response_json.get("refresh_token"),
            expires_in=response_json.get("expires_in"),
            expires_at=datetime.datetime.now() + datetime.timedelta(seconds=response_json.get("expires_in")),
            scope=response_json.get("scope"),
        )

    @staticmethod
    def get_entities(token: Token):
        headers = {
            "Authorization": f"Bearer {token.access_token}",
        }

        data = {
            "app_type": "app_camera",
            "app_version": "4.1.1.3",
            "device_types": [
                "BNMH",
                "BNCX",
                "BFII",
                "BPAC",
                "BPVC",
                "BNC1",
                "BDIY",
                "BNHY",
                "NACamera",
                "NOC",
                "NDB",
                "NSD",
                "NCO",
                "NDL"
            ],
            "sync_measurements": False
        }

        response = requests.get(f"{ExternalApi.HOST}/homesdata", headers=headers, json=data)

        if response.status_code > 299:
            raise ExternalApiException("Login failed")

        response_json = response.json()

        return [
            Entity(
                id=entity["id"],
                type=entity["type"],
                name=entity["name"],
                bridge=entity["bridge"],
                home_id=home["id"],
                home_name=home["name"],
            )
            for home in response_json["body"]["homes"] for entity in home["modules"]]

    @staticmethod
    def trigger_action(entity: Entity, token: Token):
        headers = {
            "Authorization": f"Bearer {token.access_token}",
        }

        action = {}

        if entity.type == "BNDL":
            action["lock"] = False
        elif entity.type == "BND1":
            action["on"] = True

        data = {
            "app_type": "app_camera",
            "app_version": "4.1.1.3",
            "home": {
                "timezone": "Europe/Rome",
                "id": entity.home_id,
                "modules": [
                    {
                        "bridge": entity.bridge,
                        "id": entity.id,
                        **action
                    }
                ]
            }
        }

        response = requests.post(f"{ExternalApi.HOST}/syncapi/v1/setstate", headers=headers, json=data)

        if response.status_code > 299:
            raise ExternalApiException("Login failed")

        return True