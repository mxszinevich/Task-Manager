build:
	docker-compose up -d --build
build-prod:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.prod.yml up -d --build
down:
	docker-compose down
tests:
	docker-compose exec app pytest
list:
	docker-compose ps
