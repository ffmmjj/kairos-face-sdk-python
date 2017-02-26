flake8:
	flake8

test: flake8
	nosetests ./tests
