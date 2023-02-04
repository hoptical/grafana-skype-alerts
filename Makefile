
skype: ## build skype notifier docker image
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up --build $(c)
