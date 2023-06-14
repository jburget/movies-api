# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /flask-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3",  "-m", "flask", "init-db"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
