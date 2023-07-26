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

declare -A SKIP

for PYBIN in /opt/python/cp3*/bin;
do
    allowfail=0
    fail=0

    npv=1.15
    PYV=$($PYBIN/python -V |grep 3.. -o)
    test $PYV = 3.8 && npv=1.18
    test $PYV = 3.9 && npv=1.19
    PYV=$($PYBIN/python -V |grep 3... -o)
    test $PYV = 3.10 && npv=1.21
    test $PYV = 3.11 && npv=1.22
    test $PYV = 3.12 && allowfail=1
    test PLAT = manylinux_2_24_i686 && allowfail=1
    $PYBIN/pip install numpy~=$npv.0 cython setuptools_scm || fail=1
    if test $fail = 1 ; then
	if test $allowfail = 1 ; then
	    SKIP["$PYV"]=1
	    continue
	fi
	exit $fail
    fi
    git checkout -- setup.cfg
    export SETUPTOOLS_SCM_PRETEND_VERSION=$($PYBIN/python3 -c 'from setuptools_scm import get_version ;print(get_version("."))')
    sed -e "s/numpy.*/numpy>=$($PYBIN/python -c 'from numpy.version import version; print(version)')/" -i setup.cfg
    grep numpy setup.cfg
    PY=$PYBIN/python make
    "${PYBIN}/pip" wheel . --no-deps --no-build-isolation -w wheelhouse/
done

for whl in wheelhouse/*.whl; do
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/../../../lib/ repair_wheel "$whl"
done

ls -l /io/wheelhouse

for PYBIN in /opt/python/cp3*/bin/; do
    PYV=$($PYBIN/python -V |grep 3... -o)
    [[ ${SKIP["$PYV"]} ]] && continue
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
