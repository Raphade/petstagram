<!-- ABOUT THE PROJECT -->
## About The Project

This project implements the petstagram app.

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Windows 11
python == ^3.10.2
pip == ^22.3.1

### Installation

This part describes the installation for windows 11.

1. open the git bash in project folder
2. install virtualenv with pip
   ```
   pip install virtualenv
   ```
3. create a virtual enviremont
   ```
   virtualenv venv
   ```
4. activate your virtual enviremont
   ```
   source venv/Scripts/activate
   ```
5. install the needed packages
   ```
   pip install -r requirements.txt
   ```

### Set up DB

This part describes how to set up the DB

1. download postgresql 15.3
   https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
2. install postgresql
   ```
   pw: ****
   port: ****
   Locale: German
   ```
3. start pgAdmin 4 and login with the pw
4. create a DB with the name "petstagram"



### Run application

This part describes how to run the application

1. activate your virtual enviremont
   ```
   source venv/Scripts/activate
   ```
2. run the server
   ```
   python <pathto>/manage.py runserver
   ```
3. to access the database open
   ```
   http://127.0.0.1:8000/admin
   ```
4. create db admin account if not created yet
   ```
   python <pathto>/manage.py createsuperuser
   ```
   follow instructions in the terminal
   Username: ****
   Password: ****
