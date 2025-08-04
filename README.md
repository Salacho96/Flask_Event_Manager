# Flask_Event_Manager
todor is madeup with Flask

## Installation
1- Clone the repository

2- Change the directory.
cd todo-events

Once you have the repository localy, you are ready to setup the venev of  the app

### VENV SETUP
python3 -m venv env-todo
source env-todo/bin/activate   # Mac/Linux
env-todo\Scripts\activate 

### REQUIREMENTS SETUP
pip3 install -r requirements.txt

API Flask in http://localhost:5000

PostgreSQL in localhost:5434

### MIGRATIONS
flask --app run db init
flask --app run db migrate -m "Initial migration"
flask --app run db upgrade

### OPEN THE SHELL
docker-compose up --build
python3 run.py

### API DOCUMENTATION
The API is documented in POSTMAN and in the swagger.yaml

# USAGE
Please FORK the postman Collection from the todor Workspace into your personal Workspace, in that way if any change is made that will not affect others.

# BACKUP USAGE
To restore the bd running in the Docker container please use the following command
ocker exec -i todo-events-db-1 psql -U postgres -d todoevents < backup_todoevents.sql

# UNIT TESTS
To run unit tests execute the following command
PYTHONPATH=. pytest -v
