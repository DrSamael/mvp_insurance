# MVP Insurance

### Run the project

1. pipenv shell
2. uvicorn src.main:app --reload

### Create admin user

python -m src.seed

### Run the tests and generate a coverage report

pytest --cov --cov-report=html
