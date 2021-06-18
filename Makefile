SHELL := /bin/bash

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: ienv
ienv: ## Initial .env
	cp .env_example .env

.PHONY: run
run: ## Run project
	docker-compose up -d

.PHONY: build
build: ## Run project
	docker-compose build --no-cache

.PHONY: sh
sh: ## Open sh in web container
	docker-compose exec web sh

