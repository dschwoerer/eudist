.PHONY: build check

build:
	python3 setup.py build_ext --inplace

check: build
	pytest

format:
	black .
	clang-format -i *xx

install: check
	python3 setup.py install --user
