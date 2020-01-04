clear
export FLASK_ENV=testing
echo $FLASK_ENV
pytest --cov=blueprints --cov-report html tests/ -s
export FLASK_ENV=development