.PHONY: all

STORAGES=docker_compose/storages.yaml

up_storages:
	docker compose --env-file .env -f ${STORAGES} up -d

down:
	docker compose --env-file .env -f ${STORAGES} down

migrate: 
	migrate -path src/gateways/postgresql/migrations -database "postgres://application:pass@localhost:45432/storagepi?sslmode=disable" up


up_app: 
	 uvicorn --factory src.rest.main:create_app --reload --host 0.0.0.0 --port 8000