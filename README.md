## Start Project
#### create .env file in root folder
#### configure with your settings
### RUN
```console
$ docker-compose -f ./docker-compose.yml up -d --build
$ docker exec -it quiz flask shell
>>> from app.extensions import db
>>> db.create_all()

```
###[Check it](http://127.0.0.1:5000/account/)
## Docker
### To build all images
```console
$ docker-compose -f ./docker-compose.yml build quiz_generator
```

### start all containers
```console
$ docker-compose -f ./docker-compose.yml up -d
```

### check status
```console
$ docker-compose -f ./docker-compose.yml ps
```


## Tests
### run tests
```console
$ docker exec -it quiz py.test
```


## Static
### build bundles
```console
$ docker exec -it quiz flask assets build
``` 

## Sentry
###in order to use or test senty register at [Sentry](https://docs.sentry.io/)
