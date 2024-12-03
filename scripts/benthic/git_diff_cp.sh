#! /bin/bash
cwd=`pwd`
echo $cwd

git diff --name-only main > git_diff.txt

rsync -avr --files-from git_diff.txt ./ ~/GitHub/infinigenBenthic

cd ${cwd}
