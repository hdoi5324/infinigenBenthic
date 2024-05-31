#!/bin/bash


overwrite="--overwrite" #--overwrite
cleanfiles="" #"--cleanup big_files"
outputfolder="trench_urchin"
num_scenes=5
pipeline_overrides=""

options=("" "compose_scene.seaweed_chance=0.8 compose_scene.fish_school_chance=0.5" "compose_scene.corals_chance=1.0" "compose_scene.kelp_chance=1.0")
#rm -fr outputs/${outputfolder}
for i in 0
do
  option=${options[i]}
  override=""
  if [ ${#option} -gt 0 ]; then
    override="--overrides ${option}"
  fi
  echo $override
  python -m infinigen.datagen.manage_jobs -- ${overwrite} ${cleanfiles} --output_folder outputs/${outputfolder} --num_scenes ${num_scenes} \
  --configs coral_reef_hd.gin ${override} --pipeline_configs local_16GB.gin monocular.gin cuda_terrain.gin hd_coral_reef_datagen.gin \
  ${pipeline_overrides}
done

#sudo shutdown -h 20
