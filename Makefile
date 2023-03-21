.PHONY: init-db
init-db:
	@docker-compose run --rm backend aerich init-db ${CMD_ARGS}

.PHONY: migrate
migrate:
	@docker-compose run --rm backend aerich migrate ${CMD_ARGS}

.PHONY: upgrade
upgrade:
	@docker-compose run --rm backend aerich upgrade ${CMD_ARGS}

.PHONY: downgrade
downgrade:
	@docker-compose run --rm backend aerich downgrade ${CMD_ARGS}


.PHONY: chown
chown:
	@sudo chown -R $(USER):$(USER) .
	@docker compose restart

.PHONY: bash
bash:
	@docker-compose exec backend bash

.PHONE: test
test:
	@docker-compose down
	@docker-compose -f docker-compose.yml -f docker-compose-test.override.yml up
	@docker-compose down

