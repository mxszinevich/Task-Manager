build:
	docker compose up -d --build
build-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
tests:
	docker compose exec app pytest
