#!/bin/bash

frames=24
output_dir="/media/data/hdoi5324/phd_data/infinigen/outputs/trench_video"
seed="2d3dc69d"
home_dir="/home/hdoi5324"
for i in 2 3
do
  from=$(($i*$frames+1))
  to=$((($i+1)*$frames))
  echo $from $to
  nice -n 20 ${home_dir}/.conda/envs/bproc/bin/python -m infinigen_examples.generate_auv_mission -- --input_folder ${output_dir}/${seed}/fine --output_folder ${output_dir}/${seed}/frames_0_0_00${from}_1 --seed ${seed} --task render --task_uniqname blendergt_0_0_00${from}_1 -g coral_reef coral_reef_hd.gin -p render.render_image_func=@flat/render_image LOG_DIR='${output_dir}/${seed}/logs' execute_tasks.frame_range=[${from},${to}] execute_tasks.camera_id=[0,1] execute_tasks.resample_idx=0

done

for i in 4
do
  from=$(($i*$frames+1))
  to=$((($i+1)*$frames))
  echo $from $to
  nice -n 20 ${home_dir}/.conda/envs/bproc/bin/python -m infinigen_examples.generate_auv_mission -- --input_folder ${output_dir}/${seed}/fine --output_folder ${output_dir}/${seed}/frames_0_0_00${from}_1 --seed ${seed} --task render --task_uniqname blendergt_0_0_00${from}_1 -g coral_reef coral_reef_hd.gin -p render.render_image_func=@flat/render_image LOG_DIR='${output_dir}/${seed}/logs' execute_tasks.frame_range=[${from},${to}] execute_tasks.camera_id=[0,1] execute_tasks.resample_idx=0

  nice -n 20 ${home_dir}/.conda/envs/bproc/bin/python -m infinigen_examples.generate_auv_mission -- --input_folder ${output_dir}/${seed}/fine --output_folder ${output_dir}/${seed}/frames_0_0_00${from}_1 --seed ${seed} --task render --task_uniqname rendershort_0_0_00${from}_1 -g coral_reef coral_reef_hd.gin -p render.render_image_func=@full/render_image LOG_DIR='${output_dir}/${seed}/logs' execute_tasks.frame_range=[${from},${to}] execute_tasks.camera_id=[0,1] execute_tasks.resample_idx=0
done


-- --output_folder /home/heather/GitHub/infinigen/outputs/nudi2_urchin/2d3dc69d/fine --input_folder /home/heather/GitHub/infinigen/outputs/nudi2_urchin/2d3dc69d/fine --seed 2d3dc69d --task populate --task_uniqname populate -g coral_reef coral_reef_hd.gin -p LOG_DIR='/home/heather/GitHub/infinigen/outputs/nudi2_urchin/2d3dc69d/logs' execute_tasks.frame_range=[1, 6] execute_tasks.camera_id=[0, 0]

--input_folder /home/heather/GitHub/infinigen/outputs/nudi2_urchin/2d3dc69d/fine --output_folder /home/heather/GitHub/infinigen/outputs/nudi2_urchin/2d3dc69d/frames_0_0_0001_1 --seed 2d3dc69d --task render --task_uniqname rendershort_0_0_0001_1 -g coral_reef coral_reef_hd.gin -p render.render_image_func=@full/render_image LOG_DIR='/home/heather/GitHub/infinigen/outputs/nudi2_urchin/2d3dc69d/logs' execute_tasks.frame_range=[1,6] execute_tasks.camera_id=[0,1] execute_tasks.resample_idx=0