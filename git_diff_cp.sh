#! /bin/bash
#git diff --name-only main > git_diff.txt


while read line; do
  if [ -f "${line}" ]; then
    cp ${line} ../infinigenBenthic/${line}

  fi
done < git_diff.txt
