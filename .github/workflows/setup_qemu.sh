set -ex

arch=$1

test $arch = "ppc64le" && arch=ppc64

if test $arch = "aarch64" || test $arch = "ppc64le" || test $arch = "s390x"
then
    sudo apt-get -y update
    sudo apt-get install qemu-system-$arch
fi
