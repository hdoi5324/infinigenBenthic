#!/bin/bash


overwrite="--overwrite" #--overwrite
cleanfiles="" #"--cleanup big_files"
outputfolder="nudi_4_2_test"
num_scenes=100
pipeline_overrides="" # "--pipeline_overrides manage_datagen_jobs.num_concurrent=2"

options=("" )
#rm -fr outputs/${outputfolder}
for i in 0
do
  option=${options[i]}
  python -m infinigen.datagen.manage_jobs -o outputs/${outputfolder} ${overwrite} ${cleanfiles} --num_scenes ${num_scenes} \
  --configs coral_reef_hd.gin --pipeline_configs local_16GB.gin monocular.gin cuda_terrain.gin hd_coral_reef_datagen.gin \
  ${pipeline_overrides}
done

#sudo shutdown -h 20
