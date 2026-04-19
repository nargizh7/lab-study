.PHONY: deploy test

deploy:
	SECRET_KEY=$(SECRET_KEY) DATABASE_URL=$(DATABASE_URL) python app.py

test:
	python -m pytest
