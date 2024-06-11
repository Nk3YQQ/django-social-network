runserver:
	python3 manage.py migrate --no-input
	python manage.py collectstatic --noinput
	gunicorn --config gunicorn_config.py config.wsgi:application

runserver-dev:
	python3 manage.py migrate --no-input
	gunicorn --config gunicorn_config.py config.wsgi:application

deploy:
	ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --tags "deploy"

run:
	ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --tags "run"

tests:
	docker-compose -f dev/docker-compose.yml up --build -d
	docker-compose exec -T app python3 manage.py test
	docker-compose exec -T app flake8 .
	docker-compose -f dev/docker-compose.yml down --volumes

celery-worker:
	celery -A config worker --loglevel=info

celery-beat:
	celery -A config beat --loglevel=info
