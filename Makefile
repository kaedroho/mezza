.PHONY: setup rebuild migrate superuser start migrations migrate format

setup: rebuild migrate ## Sets up development environment
	docker compose run client npm install

rebuild: ## Rebuilds the docker containers
	docker compose pull
	docker compose build

migrate: ## Run Django migrations
	docker compose run server django-admin migrate

superuser: ## Create a superuser
	docker compose run server django-admin createsuperuser

start: ## Starts the docker containers
	docker compose up

migrations: ## Create Django migrations
	docker compose run server django-admin makemigrations

migrate: ## Run Django migrations
	docker compose run server django-admin migrate

format: ## Formats and lints the code
	docker compose run server ruff format
	docker compose run server ruff check --select I --fix
	docker compose run server ruff check --fix
