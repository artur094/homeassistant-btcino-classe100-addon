import argparse
import json

from flask import Flask, jsonify, current_app

from lib.dto import User
from lib.external_api import ExternalApi
from lib.storage import Storage

app = Flask(__name__)

@app.route('/entities', methods=['GET'])
def entities():
    username = current_app.config['USERNAME']
    password = current_app.config['PASSWORD']
    client_secret = current_app.config['CLIENT_SECRET']

    retrieved_entities = ExternalApi.get_entities(User(username, password, client_secret))
    Storage.store_entities(retrieved_entities)

    return jsonify([
        entity.to_json() for entity in retrieved_entities
    ])

@app.route('/trigger/<entity_id>', methods=['POST'])
def trigger(entity_id):
    username = current_app.config['USERNAME']
    password = current_app.config['PASSWORD']
    client_secret = current_app.config['CLIENT_SECRET']

    retrieved_entities = Storage.get_entities()
    entity = next(entity for entity in retrieved_entities if entity.id == entity_id)

    ExternalApi.trigger_action(User(username, password, client_secret), entity)

    return '', 204


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
    )

    app.run(host="0.0.0.0", port=5000, debug=True)
