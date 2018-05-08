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
$ docker exec -it quiz
```


## Static
### build bundles
```console
$ docker exec -it quiz flask assets build
``` 
