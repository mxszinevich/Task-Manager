build-dev:
	docker compose up -d --build
tests:
	docker compose exec app pytest
