include .env

up:
	docker-compose up -d

upb:
	docker-compose up -d --force-recreate --build

stop:
	docker-compose stop

db:
	export PGPASSWORD=${POSTGRES_PASSWORD}; docker exec -it vms_db psql -U $(POSTGRES_USER) ${POSTGRES_DB}

test:
	docker exec -it test_api pytest 

b:
	docker exec -it $(c) /bin/bash
