#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
set -e

USERNAME=$(bashio::config 'username')
PASSWORD=$(bashio::config 'password')
CLIENT_SECRET=$(bashio::config 'client_secret')
SUPERVISOR_TOKEN=$(bashio::config 'SUPERVISOR_TOKEN')

python3 /app/main.py --username $USERNAME --password $PASSWORD --client_secret $CLIENT_SECRET