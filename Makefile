# --- development
dev:
	docker-compose up

# --- production
prod:
	docker-compose -f docker-compose.production.yml up -d
prod_down:
	docker-compose -f docker-compose.production.yml down
prod_stop:
	docker-compose -f docker-compose.production.yml stop

# --- front install packages and build
install_front:
	docker-compose -f docker-compose.builder.yml run --rm install
build_front:
	docker-compose -f docker-compose.builder.yml run --rm build

# --- containers commands (to connect and get logs)
cbe: # connect to backend container
	docker-compose exec backend /bin/bash
cdb: # connect to database container
	docker-compose exec db /bin/bash
lbe: # log backend container
	docker-compose logs -f backend
