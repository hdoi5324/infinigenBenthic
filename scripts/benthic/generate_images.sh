!/usr/bin/env bash


overwrite="--overwrite" #--overwrite
cleanfiles="" #"--cleanup big_files"
outputfolder="trench_video"
num_scenes=3
pipeline_overrides=""

options=("compose_scene.seaweed_chance=1.0" "compose_scene.kelp_chance=1.0")
#rm -fr outputs/${outputfolder}
for i in 1
do
  option=${options[i]}
  n=${#option}
  echo $n
  override=""
  if [ n > 0 ]; then
    override="--overrides ${option}"
  fi
  echo $override
  python -m infinigen.datagen.manage_jobs -- ${overwrite} ${cleanfiles} --output_folder outputs/${outputfolder} --num_scenes ${num_scenes} \
  --configs coral_reef_hd.gin ${override} --pipeline_configs local_16GB.gin monocular.gin cuda_terrain.gin hd_coral_reef_datagen.gin \
  ${pipeline_overrides}
done

#sudo shutdown -h 20
