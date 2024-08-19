#!/bin/bash

combined="/home/heather/phd_data/infinigen/collated_outputs/urchinf_rov_v1/"

if [ ! -d "$combined" ]; then
  mkdir ${combined}
fi

cd ${combined}
declare -a arr=("trench_urchinrov1" "nudi_urchinrov1")

for source in "${arr[@]}"
do
  for f in `ls /home/heather/phd_data/infinigen/collated_outputs/${source}/`
  do
    ln -s /home/heather/phd_data/infinigen/collated_outputs/${source}/${f}
  done
done
