# pull official image
FROM python:3.9-slim

# set work directory
WORKDIR usr/src/flask_app
COPY requirements.txt .
# install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .