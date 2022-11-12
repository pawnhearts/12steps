FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get upgrade -y

#RUN apt-get install -y gdal-bin libgdal-dev
#RUN apt-get install -y python3-gdal
#RUN apt-get install -y binutils libproj-dev
RUN apt-get install -y postgresql-client

COPY . /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
