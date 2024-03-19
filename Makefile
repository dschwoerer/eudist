.PHONY: build check
PY ?= python3

build: eudist.pyx
	$(PY) setup.py build_ext --inplace

check: build
	$(PY) -m pytest eudist/

format:
	black .
	clang-format -i *xx

install: check
	$(PY) setup.py install --user

install-without-check: build
	$(PY) setup.py install --user

publish: check
	rm -rf dist
	$(PY) -m pip install --user --upgrade setuptools wheel twine
	$(PY) setup.py sdist bdist_wheel
	$(PY) -m twine upload  --repository testpypi dist/eudist*.tar.gz

deps:
	$(PY) -m ensurepip
	$(PY) -m pip install setuptools Cython numpy setuptools_scm pytest
