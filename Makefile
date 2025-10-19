.PHONY: help build up down logs clean restart redis-cli cache-clear

help:
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build:
	docker-compose build

up:
	@echo "Application starting..."
	docker-compose up --build -d
	@echo "Run 'make logs' to view the server logs."

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

clean:
	docker-compose down -v --rmi all

redis-cli:
	docker-compose exec api.redis redis-cli

cache-clear:
	docker-compose exec api.redis redis-cli FLUSHALL
	@echo "Cache cleared"

