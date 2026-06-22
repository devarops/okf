.PHONY: \
  clean \
  init \
  install \
  setup \
  tests

clean:
	rm --force --recursive tests/__pycache__

init: setup tests

install:
	pip install --editable .

setup: clean install

tests:
	pytest --verbose tests



