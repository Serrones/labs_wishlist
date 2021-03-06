# Labs WishList

Web Server API Restful with Flask framework

Integrating with Flask-SQLAlchemy extension

## Flask and Extensions

- FLASK: [Flask](http://flask.pocoo.org/)

- SQL ORM: [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.3/)

## Tests and Logs

- LOGGING: [Python logging](https://docs.python.org/3/library/logging.html)

- Testing: [Python unittest](https://docs.python.org/3/library/unittest.html)

- Coverage: [Coverage.py](https://docs.python.org/3/library/unittest.html)

## Databases

- Development localhost: [SQLite](https://www.sqlite.org/docs.html)

- Testing: [SQLite](https://www.sqlite.org/docs.html)

- Docker Environment: [Postgres](https://www.postgresql.org/)

## Flask Project

Cloning repository:
```
git clone https://github.com/Serrones/labs_wishlist
```
## Install requirements

Python version:
```
3.9.0
```
Create a virtual environment:
```
python3 -m venv .venv
```
Enable virtual environment:
```
source .venv/bin/activate
```
Install requiriments with pip:
```
pip install -r requirements.txt
```

### Running Flask with command line

Initializing Flask Project:
```
export FLASK_APP=labs_wishlist.py
export FLASK_DEBUG=1
```
Upgradind database:
```
make upgrade
```
Running service:
```
make run
```

## Tests

Running tests:
```
make test
```
Running tests and generate coverage report:
```
make test-coverage
```
Verify lint:
```
make lint
```
Shell with flask project context:
```
make shell
```
### Running Docker

Create an App Container:
```
make docker-flask
```
Running App and Postgres database:
```
make docker-compose
```
Upgradind database:
```
From another shell window:
    docker ps (To get container id from labs_wishlist_web_1)
    docker exec -i -t <labs_wishlist_web_1 id> bash
    make upgrade
```
## Documentation

Open file `index.html` in a browser:
```
docs/index.html
```

## Authentication and Permissions

Generate token:
```
Authorization Basic Auth
(username and password)
```
Create User:
```
You dont need authentication to create an User
```
Update and Delete User:
```
You need authentication to update and delete an User 

If an User has is_admin true, he has permission to update and delete an User
```
Get User, Get Users, Get Product and Remove Product:
```
You need authentication to get an User or an User list 
```
