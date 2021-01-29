# pull official image
FROM python:3.9-slim

# set work directory
ENV CONTAINER_HOME=/var/www
ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

# install dependencies
RUN pip3 install -r $CONTAINER_HOME/requirements.txt