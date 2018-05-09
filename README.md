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
$ docker exec -it quiz nosetests -v
```


## Static
### build bundles
```console
$ docker exec -it quiz flask assets build
``` 

## Sentry
###in order to use or test senty register at [Sentry](https://docs.sentry.io/)
