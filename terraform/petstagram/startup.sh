#!/bin/bash
apt-get update
apt-get install -y python3-pip python3-dev build-essential libssl-dev libffi-dev nginx
sudo /etc/init.d/nginx start    # start nginx
python - m pip install https://projects.unbit.it/downloads/uwsgi-lts.tar.gz
pip3 install virtualenv

git clone https://github.com/pfad/zur/app /opt/petstagram
cd /opt/petstagram

virtualenv venv
source venv/bin/activate
pip install django
pip install -r requirements.txt

# PostgreSQL-Verbindungseinstellungen
export DB_HOST="/cloudsql/${GOOGLE_CLOUD_PROJECT}:${REGION}:${INSTANCE}"
export DB_NAME="database"
export DB_USER="database-user"
export DB_PASSWORD="your_password"

# configure uwsgi
echo "[uwsgi]
chdir = /opt/petstagram
module = petstagram.wsgi:application
home = /opt/petstagram/venv
master = true
processes = 5
socket = /opt/petstagram/mysite.sock
chmod-socket = 664
pidfile = /tmp/project-master.pid
max-requests = 5000
vacuum = true
daemonize = /var/log/uwsgi/petstagram.log
env = LANG=en_US.UTF-8
" > /etc/uwsgi.d/petstagram_uwsgi.ini

# Configure Nginx
echo "upstream django {
    server unix:///opt/petstagram/mysite.sock;
}

server {
    listen 80;
    server_name example.com;

    location / {
        uwsgi_pass django;
        include uwsgi_params;
    }

    location /static/ {
        alias /opt/petstagram/static/;
    }

    location /media/ {
        alias /opt/petstagram/media/;
    }
}
" > /etc/nginx/sites-available/petstagram

# restart nginx
service nginx restart

# Django-App mit uWSGI starten
sudo uwsgi --ini /etc/uwsgi.d/petstagram_uwsgi.ini
