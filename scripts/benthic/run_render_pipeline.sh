#!/bin/bash

frames=1
output_dir="/home/heather/GitHub/infinigen/outputs/nudi_urchin3"
home_dir="/home/heather"

for seed in 63040821 1595e93e 675a31da 6723a8ee 70e5b232 279e08b4 78ee6790 c3e681b 92794e9 53623e69 5d98521e e3629e2 1e611603 3813d192 4a1fb6a6
do
  for from in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
  do
    echo $from $seed
    nice -n 20 ${home_dir}/.conda/envs/bproc/bin/python -m infinigen_examples.generate_auv_mission -- --input_folder ${output_dir}/${seed}/fine \
    --output_folder ${output_dir}/${seed}/frames_0_0_00${from}_1 --seed ${seed} --task render --task_uniqname rendershort_0_0_00${from}_1 \
    -g coral_reef coral_reef_hd.gin -p render.render_image_func=@full/render_image LOG_DIR='${output_dir}/${seed}/logs' execute_tasks.frame_range=[${from},${from}] execute_tasks.camera_id=[0,1] execute_tasks.resample_idx=0
  done
  
  for from in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
  do
    echo $from $seed
    nice -n 20 ${home_dir}/.conda/envs/bproc/bin/python -m infinigen_examples.generate_auv_mission -- --input_folder ${output_dir}/${seed}/fine \
    --output_folder ${output_dir}/${seed}/frames_0_0_00${from}_1 --seed ${seed} --task render --task_uniqname blendergt_0_0_00${from}_1 -g coral_reef coral_reef_hd.gin \
    -p render.render_image_func=@flat/render_image LOG_DIR='${output_dir}/${seed}/logs' execute_tasks.frame_range=[${from},${from}] execute_tasks.camera_id=[0,1] execute_tasks.resample_idx=0
  
  done
done
