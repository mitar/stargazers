#!/bin/bash -e

source ~/.virtualenv/stargazers/bin/activate

rm -f lists.new

./stargazers.py > lists.new

sort -u lists.new > lists.$(date +%s)
rm lists.new

diff -i -w --unchanged-group-format='' --old-group-format='' --new-group-format='%>' --changed-group-format='' $(ls -1 lists.* | tail -n 2)
