.PHONY: all clean docs docs-serve lint type test test-cov

CMD:=
PYMODULE:=pyinv
MANAGEPY:=$(CMD) ./$(PYMODULE)/manage.py
APPS:=assets pyinv
SPHINX_ARGS:=docs/ docs/_build -nWE

all: type test check lint

lint: 
	$(CMD) flake8 $(PYMODULE) $(TESTS)

check:
	$(MANAGEPY) check

dev:
	$(MANAGEPY) runserver

docs:
	$(CMD) sphinx-build $(SPHINX_ARGS)

docs-serve:
	$(CMD) sphinx-autobuild --port 8001 $(SPHINX_ARGS)

type: 
	cd pyinv && mypy $(APPS)

test: | $(PYMODULE)
	cd pyinv && pytest --cov=. $(APPS) $(PYMODULE)

test-cov:
	cd pyinv && pytest --cov=. $(APPS) $(PYMODULE) --cov-report html

isort:
	$(CMD) isort $(PYMODULE) $(TESTS)

clean:
	git clean -Xdf # Delete all files in .gitignore
