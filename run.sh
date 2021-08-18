#!/bin/bash

set -e
set -x

REVS=( "2.6.3"  "2.6.0" "2.5.4" )

if [ ! -d "dvc" ]; then
  git clone https://github.com/iterative/dvc
fi

for REV in ${REVS[@]}; do
  pushd dvc
  git checkout $REV
  pip install -e '.[all,tests]'
  popd

  pytest --benchmark-save $REV $@
done