CONDA_ENV ?= portfolio_management

test:
	@pytest -s .

env.create:
	@conda create -y -n ${CONDA_ENV} python=3.7

env.update:
	@conda env update -n ${CONDA_ENV} -f environment.yml

