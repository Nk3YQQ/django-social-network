runserver:
	python3 manage.py migrate --no-input
	python manage.py collectstatic --noinput
	gunicorn --config gunicorn_config.py config.wsgi:application

runserver-dev:
	python3 manage.py migrate --no-input
	python3 manage.py runserver 0.0.0.0:8000

deploy-project:
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose.yml up --build -d

deploy:
	ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --tags "deploy"

run:
	ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --tags "run"

tests:
	docker-compose -f docker-compose.dev.yml up --build -d
	docker-compose ps
	docker-compose logs -f app
	docker-compose exec -T app python3 manage.py test
	docker-compose exec -T app flake8 .
	docker-compose -f docker-compose.dev.yml down --volumes

celery-worker:
	celery -A config worker --loglevel=info

celery-beat:
	celery -A config beat --loglevel=info
