DOCKER_COMPOSE_FILE = docker-compose.yml
CI_DOCKER_COMPOSE_FILE = ci/docker-compose.yml
GIT_COMMIT ?= $(shell git rev-parse --short HEAD)
SERVICE ?= api

.PHONY: up build logs format ps down
.PHONY: ci/run ci/build ci/ps ci/test ci/down

install: # 

up: # Start containers
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d --build --force-recreate

build: # Build containers
	docker-compose -f $(DOCKER_COMPOSE_FILE) build

format: # Format code
	poetry run black .
	poetry run flake8

logs: # Tail the service container's logs
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs -tf $(SERVICE)

ps: #: Show running processes
	docker-compose -f $(DOCKER_COMPOSE_FILE) ps

down: # Bring down the service
	docker-compose -f $(DOCKER_COMPOSE_FILE) down
	

ci/run: # Run continuous integration
	./ci/scripts/run.sh

ci/build:
	docker-compose -f $(CI_DOCKER_COMPOSE_FILE) build

ci/ps: #: Show running processes
	docker-compose -f $(CI_DOCKER_COMPOSE_FILE) ps

ci/test:
	docker-compose -f $(CI_DOCKER_COMPOSE_FILE) build
	docker-compose -f $(CI_DOCKER_COMPOSE_FILE) run tests
	docker-compose -f $(CI_DOCKER_COMPOSE_FILE) run tests flake8

ci/down:
	docker-compose -f $(CI_DOCKER_COMPOSE_FILE) down