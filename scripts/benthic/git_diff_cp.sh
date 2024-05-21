#! /bin/bash
cwd=`pwd`
echo $cwd

cd ~/GitHub/infinigen

git diff --name-only main > git_diff.txt

rsync -av --files-from git_diff.txt ~/GitHub/infinigen/ ~/GitHub/infinigenBenthic

cd ${cwd}
