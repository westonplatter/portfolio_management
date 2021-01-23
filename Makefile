CONDA_ENV ?= portfolio_management
ENV ?= development
FLASK_APP ?=api.app

.PHONY: all test clean


###############################################################################
# run time
#
run.be:
	@python server.py

run.fe:
	@yarn run start


###############################################################################
# tests
#
test:
	ENV=test pytest -s .

eslint:
	yarn run eslint api/static/js


###############################################################################
# conda env
#
env.create:
	@conda create -y -n ${CONDA_ENV} python=3.7

env.update:
	@conda env update -n ${CONDA_ENV} -f environment.yml


###############################################################################
# db operations
#
db.migrate:
	ENV=${ENV} FLASK_APP=${FLASK_APP} flask db migrate

db.upgrade:
	ENV=${ENV} FLASK_APP=${FLASK_APP} flask db upgrade

db.downgrade:
	ENV=${ENV} FLASK_APP=${FLASK_APP} flask db downgrade

db.truncate:
	@psql \
		-d portfolio_manager_dev \
		-c "truncate trades;"

db.drop:
	@psql \
		-d portfolio_manager_dev \
		-c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
