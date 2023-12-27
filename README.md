# SWANPRO
This is a practice work for swanpro.

# Environment Requirement
- python v3.x
- MySQL v8.x

# Environment Tested On
- Ubuntu 20.04 INTEL PROCESSOR

# How to run this project
### Clone the project and move (cd) into the project's directory
```bash
git clone https://github.com/Maxcarrassco/swanpro-practice && cd swanpro-practice
```
### create and activate your virtual environment, and install the project dependencies
```bash
# create virtual environment
python3 -m venv venv
# activate virtual environment
source venv/bin/activate
# install dependencies
pip install -r requirement.txt
```
### Create your environment file (.env) and place your database connection string in it
```bash
# from the root of the project
touch .env
# inside .env file
DB_URL=mysql://{YOUR_DB_USER_NAME}:{YOUR_DB_PASSWORD}@{HOST}:{PORT}/{DBNAME} # ensure to create a database
             OR
DB_URL=postgres://{YOUR_DB_USER_NAME}:{YOUR_DB_PASSWORD}@{HOST}:{PORT}/{DBNAME} # ensure to create a database
```
### Command to start the API Server
```bash
# inside the backend directory
python3 -m api.v1.app
```
