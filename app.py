from flask import Flask, request
import db

app = Flask(__name__)
app.config.from_mapping(DATABASE="db.sqlite3")
db.init_app(app)


@app.route('/')
def hello():
    return "Hello, world!"


if __name__ == '__main__':
    app.run()
