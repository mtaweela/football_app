dev:
	docker-compose up

# containers commands
cbe: # connect to backend container
	docker-compose exec backend /bin/bash
cdb: # connect to database container
	docker-compose exec db /bin/bash
lbe: # log backend container
	docker-compose logs -f backend
