# movies-api
Simple REST API server with movie database

## Linux installation
```bash
git clone https://github.com/jburget/movies-api.git
cd movies-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask init-db # initiate sqlite3 database, note that any existing data will be lost
flask run
```

## Windows installation
If you are using Windows, please switch to Linux and continue with steps above.

## Docker installation
```bash
# build the image
docker build https://github.com/jburget/movies-api.git#main --tag movies-api
# run the container
docker run --rm -p 5000:5000 --name movies-api movies-api
```
## Run tests with pytest
```bash
pip install -r test-requirements.txt
python -m pytest --color=yes
```

## Usage
You can use browser at http://localhost:5000 or try my shell client
* make script executable with `chmod u+x ./curl-client.sh`
* run script in current environment `source ./curl-client.sh`, hint will appear.
* function post-movie sets shell variable `LAST_POSTED_ID` to the new record id
* see other script variables `head --lines=7 ./curl-client.sh`

## Shell client usage
```bash
$ source ./curl-client.sh
Usage: post-movie <title> <release_year> [description]
       sets shell variable LAST_POSTED_ID to id of the new movie record
Usage: get-movies [id]
Usage: edit-movie <id> <title> <release_year> [description]
```

Some parts of the code may come from the official [Flask](https://flask.palletsprojects.com/) or [sqlite3](https://docs.python.org/3/library/sqlite3.html) documentation
