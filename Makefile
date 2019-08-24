# vi: ft=make

.PHONY: check
check:
	isort --recursive --check-only kformat tests
	black -S -l 79 --check kformat tests

.PHONY: format
format:
	isort -rc -y kformat tests
	black -S -l 79 kformat tests

.PHONY: test
test:
	python -m pytest

.PHONY: lint
coverage:
	python -m  pytest --cov kformat --cov-branch
