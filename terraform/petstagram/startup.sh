#!/bin/bash
apt-get update
apt-get install -y python3-pip python3-dev build-essential libssl-dev libffi-dev
pip3 install virtualenv

git clone https://github.com/pfad/zur/app /opt/petstagram
cd /opt/petstagram

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt

# PostgreSQL-Verbindungseinstellungen
export DB_HOST="/cloudsql/${GOOGLE_CLOUD_PROJECT}:${REGION}:${INSTANCE}"
export DB_NAME="database"
export DB_USER="database-user"
export DB_PASSWORD="your_password"

# Django-App mit uWSGI starten
uwsgi --http :8000 --wsgi-file wsgi.py --master --processes 4 --threads 2 --stats :1717