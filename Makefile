.PHONY: install test run lint clean

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=. --cov-report=html

run:
	python run_api.py

lint:
	python -m flake8 .
	python -m black --check .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf *.db
