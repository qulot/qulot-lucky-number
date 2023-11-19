# Lucky Number Service

lucky-number-service contains a quantum algorithm for generating absolutely random lucky numbers

## Run

Next we need to update the gRPC code used by our application to use the new service definition.

```
uvicorn main:app --port 8080 --log-config uvicorn_log_conf.yaml
```

## Docker

To make it easier to deploy the service, we use Docker to build the source code into a (docker)[https://docs.docker.com/engine/reference/commandline/build/] image

```
make build-docker
```


Run docker image
```
make run-docker
```