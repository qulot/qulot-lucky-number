APP_VERSION := latest
DOCKER_TAG := 270498/lnsvc:$(APP_VERSION)

proto:
	python \
		-m grpc_tools.protoc \
		-I=protobuf/ \
		--python_out=src/lucky_number/proto \
		--grpc_python_out=src/lucky_number/proto \
		protobuf/*.proto

	cd src/lucky_number/proto && sed -i '' 's/^\(import.*pb2\)/from . \1/g' *.py

build:
	docker build . -t $(DOCKER_TAG)

push:
	docker push $(DOCKER_TAG)

deploy:
	make build
	make push

run-docker:
	docker run -d --name qulot-luckynumber-$(APP_VERSION) -p 3051:8000 $(DOCKER_TAG)

run-dapr:
	cd src && dapr run -a luckynumber -p 8086 -P grpc -- python main.py