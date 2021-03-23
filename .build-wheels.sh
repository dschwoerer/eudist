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

for PYBIN in /opt/python/cp3*/bin;
do
    npv=1.15
    test $($PYBIN/python -V |grep 3.. -o) == 3.9 && npv=1.18
    $PYBIN/pip install numpy==$npv cython setuptools_scm
    git checkout -- setup.cfg
    export SETUPTOOLS_SCM_PRETEND_VERSION=$($PYBIN/python3 -c 'from setuptools_scm import get_version ;print(get_version("."))')
    sed -e "s/numpy.*/numpy>=$($PYBIN/python -c 'from numpy.version import version; print(version)')/" -i setup.cfg
    grep numpy setup.cfg
    PY=$PYBIN/python make
    "${PYBIN}/pip" wheel . --no-deps -w wheelhouse/
done

for whl in wheelhouse/*.whl; do
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/../../../lib/ repair_wheel "$whl"
done

ls -l /io/wheelhouse

for PYBIN in /opt/python/cp3*/bin/; do
    "${PYBIN}/pip" install $NAME --no-index -f /io/wheelhouse
    if test -e "${PYBIN}/nosetests"
    then
	(
	    cd "$HOME"
	    "${PYBIN}/nosetests" $NAME
	)
    fi
done

ls -l wheelhouse || :
mkdir -p wheelhouse
rm -f wheelhouse/*whl
ls -l wheelhouse
cp /io/wheelhouse/*whl wheelhouse/
ls -l wheelhouse
