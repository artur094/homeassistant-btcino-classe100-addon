import argparse
import json

from flask import Flask, jsonify, current_app

from lib.external_api import ExternalApi
from lib.storage import Storage

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    username = current_app.config['USERNAME']
    password = current_app.config['PASSWORD']
    client_secret = current_app.config['CLIENT_SECRET']
    storage_file = current_app.config['STORAGE_FILE']

    token = current_app.config['TOKEN']

    if token is None:
        token = Storage.get_token(storage_file)

    token = ExternalApi.login(username, password, client_secret, token)
    Storage.store_token(token, storage_file)
    current_app.config['TOKEN'] = token.access_token

@app.route('/entities', methods=['GET'])
def entities():
    token = current_app.config['TOKEN']
    storage_file = current_app.config['STORAGE_FILE']

    entities = ExternalApi.get_entities(token)
    Storage.store_entities(entities, storage_file)

    return jsonify(json.dumps(entities))

@app.route('/trigger/<entity_id>', methods=['POST'])
def trigger(entity_id):
    token = current_app.config['TOKEN']
    storage_file = current_app.config['STORAGE_FILE']

    entities = Storage.get_entities(storage_file)
    entity = next(entity for entity in entities if entity.id == entity_id)

    ExternalApi.trigger_action(token, entity)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Btcino - Home Assistant integration')
    parser.add_argument('--username', type=str, required=True, help='Username')
    parser.add_argument('--password', type=str, required=True, help='Password')
    parser.add_argument('--client_secret', type=str, required=True, help='Btcino Client Secret')

    args = parser.parse_args()

    app.config.update(
        USERNAME=args.username,
        PASSWORD=args.password,
        CLIENT_SECRET=args.client_secret,
        STORAGE_FILE="/data/storage.json"
    )

    app.run(host="0.0.0.0", port=5000, debug=True)
