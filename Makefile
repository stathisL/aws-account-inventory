.PHONY: test run

test:
	python -m pytest -v

run:
	python -m src.inventory
