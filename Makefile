# .PHONY: install test run lint clean
#
# install:
# 	pip install -r requirements.txt
#
# test:
# 	pytest tests/ -v --cov=. --cov-report=html
#
# run:
# 	python run_api.py
#
# lint:
# 	python -m flake8 .
# 	python -m black --check .
#
# clean:
# 	find . -type d -name "__pycache__" -exec rm -rf {} +
# 	find . -type f -name "*.pyc" -delete
# 	rm -rf htmlcov/
# 	rm -rf .pytest_cache/
# 	rm -rf *.db


.PHONY: install test run lint clean docker-build docker-run docker-stop docker-clean

# Development
install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing

run:
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	black --check .
	mypy . --ignore-missing-imports

format:
	black .
	isort .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf *.db
	rm -rf logs/*.log

# Docker
docker-build:
	docker-compose build

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-clean:
	docker-compose down -v
	docker system prune -f

docker-test:
	docker-compose run --rm test

# Production
deploy:
	./deploy.sh

backup:
	mkdir -p backups
	docker exec aircraft-data-db pg_dump -U aircraft aircraft_data > backups/db_$(shell date +%Y%m%d_%H%M%S).sql

# CI/CD
ci: lint test

cd: docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  install       - Install Python dependencies"
	@echo "  test          - Run test suite with coverage"
	@echo "  run           - Run development server"
	@echo "  lint          - Run linters"
	@echo "  format        - Format code"
	@echo "  clean         - Clean temporary files"
	@echo "  docker-build  - Build Docker images"
	@echo "  docker-run    - Start Docker containers"
	@echo "  docker-stop   - Stop Docker containers"
	@echo "  docker-logs   - View Docker logs"
	@echo "  deploy        - Deploy to production"
	@echo "  backup        - Create database backup"
