#!/bin/bash


overwrite="--overwrite" #--overwrite
cleanfiles="" #"--cleanup big_files"
outputfolder="nudi_urchin3"
num_scenes=15
pipeline_overrides="" # "--pipeline_overrides manage_datagen_jobs.num_concurrent=2"

options=("" )
#rm -fr outputs/${outputfolder}
for i in 0
do
  option=${options[i]}
  override="" # "--overrides ???"
  echo $override
  python -m infinigen.datagen.manage_jobs -- ${overwrite} ${cleanfiles}  --debug --output_folder outputs/${outputfolder} --num_scenes ${num_scenes} \
  --configs coral_reef_hd.gin ${override} --pipeline_configs local_16GB.gin monocular.gin cuda_terrain.gin hd_coral_reef_datagen.gin \
  ${pipeline_overrides}
done

#sudo shutdown -h 20
