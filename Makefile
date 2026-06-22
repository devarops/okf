.PHONY: \
  clean \
  tests

clean:
	rm --force --recursive tests/__pycache__

tests:
	pytest --verbose tests
