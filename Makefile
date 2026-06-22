.PHONY: \
  clean \
  init \
  install \
  setup \
  tests \
  validate

clean:
	rm --force --recursive tests/__pycache__

init: setup tests

install:
	pip install --editable .

setup: clean install

tests:
	pytest --verbose tests

validate:
	python -c "import okf; print(okf.validate())"
