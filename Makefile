.PHONY: build check
PY ?= python3

build: eudist.pyx
	python3 setup.py build_ext --inplace

eudist.pyx: eudist.pyx.in
	PY=$(PY) bash $< > $@.tmp
	mv $@.tmp $@

check: build
	python -m pytest eudist/

format:
	black .
	clang-format -i *xx

install: check
	python3 setup.py install --user

install-without-check: build
	python3 setup.py install --user

publish: check
	rm -rf dist
	python3 -m pip install --user --upgrade setuptools wheel twine
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload  --repository testpypi dist/eudist*.tar.gz
