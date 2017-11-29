.PHONY: build start stop test

build:
	docker build . -t test_service

start:
	docker run -p 80:8000 -d --name test_service_1 test_service runserver

stop:
	docker stop test_service_1
	docker rm test_service_1

test:
	docker run --rm test_service runtests
