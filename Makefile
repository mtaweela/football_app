dev:
	docker-compose up

prod:
	docker-compose -f docker-compose.production.yml

install:
	docker-compose -f docker-compose.builder.yml run --rm install

# containers commands
cbe: # connect to backend container
	docker-compose exec backend /bin/bash
cdb: # connect to database container
	docker-compose exec db /bin/bash
lbe: # log backend container
	docker-compose logs -f backend
