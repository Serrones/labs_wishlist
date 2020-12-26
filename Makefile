upgrade:
	flask db upgrade

test:
	pytest -x --ignore postgres/

lint:
	flake8 --show-source app/
	isort --check-only app/
	mypy app/

fix-import:
	isort app/

test-coverage:
	coverage run --source app/ -m pytest -x --ignore postgres/
	coverage report -m

run:  # First run this command --> export FLASK_APP=labs_wishlist.py
	flask run

shell:
	flask shell
