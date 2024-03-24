migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

superuser:
	python3 manage.py createsuperuser --username="a" --email="a@a.com"

runserver:
	python3 manage.py runserver