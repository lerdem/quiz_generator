FROM python:3.6
MAINTAINER Dmytro Kaminskiy "dmytro.kaminskyi92@gmail.com"
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends python-setuptools python-dev
COPY . /project
WORKDIR /project

RUN pip install --upgrade pip==10.0.1
RUN pip install -r ./requirements/development.txt

#RUN chmod 777 -R logs
#RUN chmod 777 -R run
#RUN chmod 777 -R migrations

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
