.PHONY: init-db
init-db:
	@docker compose run --rm backend aerich init-db ${CMD_ARGS}

.PHONY: migrate
migrate:
	@docker compose run --rm backend aerich migrate ${CMD_ARGS}

.PHONY: upgrade
upgrade:
	@docker compose run --rm backend aerich upgrade ${CMD_ARGS}

.PHONY: downgrade
downgrade:
	@docker compose run --rm backend aerich downgrade ${CMD_ARGS}


.PHONY: chown
chown:
	@docker compose run --rm -u root backend chown -R $$(id -u):$$(id -g) /backend
	@docker compose run --rm -u root backend chown -R $$(id -u):$$(id -g) /requirements


.PHONY: bash
bash:
	@docker-compose exec backend bash

.PHONE: test
test:
	@docker compose down
	@docker compose -f docker-compose.yml -f docker-compose-test.override.yml run --rm backend /scripts/run_tests.sh ${CMD_ARGS}
	@docker compose down

.PHONY: pip-compile
pip-compile:
	@docker compose run --rm -u root backend pip-compile --allow-unsafe --generate-hashes --output-file=/requirements/requirements.txt /requirements/requirements.in --resolver=backtracking ${CMD_ARGS}
	@docker compose run --rm -u root backend chown -R $$(id -u):$$(id -g) /requirements

.PHONY: lint
lint:
	@echo "Sorting requirements..."
	@docker compose run --rm backend python /scripts/sort_requirements.py
	@echo "Sorting imports..."
	@docker compose run --rm backend isort /backend --profile black --line-length 120
