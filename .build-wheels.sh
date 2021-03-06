set -ex

export NAME=eudist

export PLAT=$1

function repair_wheel {
    wheel="$1"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" --plat "$PLAT" -w /io/wheelhouse/
    fi
}

for PYBIN in /opt/python/*/bin;
do
    make clean
    $PYBIN/pip install numpy cython
    PY=$PYBIN/python make
    "${PYBIN}/pip" wheel . --no-deps -w wheelhouse/
done

for whl in wheelhouse/*.whl; do
    LD_LIBRARY_PATH=$(realpath ../../../lib/) repair_wheel "$whl"
done

ls -l /io/wheelhouse

for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install $NAME --no-index -f /io/wheelhouse
    if test -e "${PYBIN}/nosetests"
    then
	(
	    cd "$HOME"
	    "${PYBIN}/nosetests" $NAME
	)
    fi
done
