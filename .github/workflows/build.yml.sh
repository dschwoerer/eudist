cat <<'EOF'
name: Build

on: [push, pull_request]

jobs:
  build_wheels:
    name: Build wheels on ${{ matrix.config.name }}
    runs-on: ${{ matrix.config.os }}
    strategy:
      fail-fast: false
      matrix:
        config:
EOF
for arch in aarch64 ppc64le s390x ; do
    for py in 36 37 38 39 310 311 312 313 ; do
        build="cp${py}* pp${py}*"
        if test $arch = s390x ; then
            # disable pp
            build="cp$py*manylinux*"
            # skip 3.11
            test $py = 311 && continue
            test $py = 313 && continue
        fi
        if test $arch = ppc64le ; then
            # skip 3.9
            test $py = 39 && continue
            test $py = 311 && continue
        fi
	if test $arch = aarch64 ; then
	    test $py = 313 && continue
	fi

        cat <<EOF
          - name: "linux $arch $py"
            os: ubuntu-latest
            arch: $arch
            build: "$build"
            pyversion: $py
EOF
    done
done
cat <<'EOF'
          - name: windoof
            os: windows-latest
            build: "*"
          - name: mac intel
            os: macos-13
            build: "*"
          - name: mac arm
            os: macos-14
            build: "*"

    steps:
      - uses: actions/checkout@v4

      - name: Set up QEMU
        if: ${{ contains(matrix.config.name, 'linux') }}
        uses: docker/setup-qemu-action@v3
        with:
          platforms: ${{ matrix.config.arch }}

      - name: Build wheels
        uses: pypa/cibuildwheel@v2.22.0
        env:
          CIBW_BUILD: ${{ matrix.config.build }}
          CIBW_SKIP: "pp*-win_amd64 pp39*linux_i686 pp31?*linux_i686"
          CIBW_ARCHS_LINUX: "${{ matrix.config.arch }}"
          # CIBW_TEST_COMMAND: pip install pytest && pytest {package}
        # with:
        #   package-dir: .
        #   output-dir: wheelhouse
        #   config-file: "{package}/pyproject.toml"

      - uses: actions/upload-artifact@v4
        with:
          name: "dist-${{ matrix.config.os }}-${{ matrix.config.arch }}-${{ matrix.config.pyversion }}"
          path: ./wheelhouse/*.whl


  make_sdist:
    name: Make SDist
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 100  # Optional, use if you use setuptools_scm
        submodules: true  # Optional, use if you have submodules

    - name: Build SDist
      run: pipx run build --sdist

    - uses: actions/upload-artifact@v4
      with:
        name: dist-sdist
        path: dist/*.tar.gz


  upload_all:
    needs: [build_wheels, make_sdist]
    environment: pypi
    permissions:
      id-token: write
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
    - uses: actions/download-artifact@v4
      with:
        path: dist
        pattern: dist-*
        merge-multiple: true

    - uses: pypa/gh-action-pypi-publish@release/v1
EOF
