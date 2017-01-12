#!/bin/bash

set -x

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$(date +%Y%m%d)
package=freshplayerplugin
branch=master
name=freshplayerplugin

pushd ${tmp}
git clone https://github.com/i-rinat/${package}.git
cd ${package}
git checkout ${branch}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=`git describe --tags | awk -F '-' '{print $1}' | tr -d 'v'`
cd ${tmp}
tar Jcf "$pwd"/${name}-${version}-${date}-${tag}.tar.xz ${package}

popd
upload_source=$( curl --upload-file ${name}-${version}-${date}-${tag}.tar.xz https://transfer.sh/${name}-${version}-${date}-${tag}.tar.xz )

if [ -n "$upload_source" ]; then
GCOM=$( sed -n '/Source0:/=' ${name}.spec)
sed -i "${GCOM}s#.*#Source0:	${upload_source}#" ${name}.spec
fi



