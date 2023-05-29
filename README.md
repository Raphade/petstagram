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

### Run application

This part describes how to run the application

1. run the server
   ```
   python <pathto>/manage.py runserver
   ```
2. to access the database open
   ```
   http://127.0.0.1:8000/admin
   ```
3. create db admin account if not created yet
   ```
   python <pathto>/manage.py createsuperuser
   ```
3. follow instructions in the terminal
