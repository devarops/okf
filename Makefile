all: check tests

.PHONY: \
  all \
  check \
  clean \
  format \
  init \
  install \
  setup \
  tests \
  validate

module = okf

check:
	black --check --line-length 100 ${module}
	black --check --line-length 100 tests
	flake8 --max-line-length 100 ${module}
	flake8 --max-line-length 100 tests
	mypy ${module}
	mypy tests

clean:
	rm --force --recursive tests/__pycache__

format:
	black --line-length 100 ${module}
	black --line-length 100 tests

init: setup tests

install:
	pip install --editable .

setup: clean install

tests:
	pytest --verbose tests

validate:
	python -c "import okf; print(okf.validate())"
