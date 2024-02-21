run:
	@poetry run uvicorn src.main:app --port 8080 --reload

run_docker:
	@docker compose --file docker-compose.dev.yml up

dropdb:
	@dropdb rinha || true

createdb: dropdb
	@createdb rinha || true
	@psql rinha --file script.sql

select_c:
	@psql rinha --command "select * from customer"

select_t:
	@psql rinha --command "select * from transaction"
