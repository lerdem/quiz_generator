FROM python:3.6
MAINTAINER Dmytro Kaminskiy "dmytro.kaminskyi92@gmail.com"
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends python-setuptools python-dev
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
