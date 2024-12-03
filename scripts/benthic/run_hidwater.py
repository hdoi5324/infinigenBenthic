from glob import glob

top_dir = "/home/heather/GitHub/infinigen/outputs"

with open(f"{top_dir}/urchininf_v0.txt", 'r') as file:
    # Read all lines into a list
    lines = file.readlines()

# Print each line
updated_commands = []
for seed in lines:
    seed = seed.strip()
    print(seed.strip())
    files = glob(f"{top_dir}/*/{seed.strip()}/run_pipeline.sh")
    with open(files[0], 'r') as file:
        # Read all lines into a list
        commands = file.readlines()
    commands = [c for c in commands if "rendershort" in c]
    for c in commands:
        c = commands[0]
        c = c.replace("rendershort", "renderhidewater")
        c = c.replace("execute_tasks.resample_idx=0", "execute_tasks.resample_idx=0 render.hide_water=True")
        c = c.replace("bproc", "infinigen")
        print(c)
        updated_commands.append(c)
print(updated_commands)

#nice -n 20 /home/heather/.conda/envs/infinigen/bin/python -m infinigen_examples.generate_auv_mission -- --input_folder /media/data/GitHub/infinigen/outputs/nudi_handfish_rov_v3/f67395a/fine --output_folder /media/data/GitHub/infinigen/outputs/nudi_handfish_rov_v3/f67395a/frames__0_0_0001_0 --seed f67395a --task render --task_uniqname renderhidewater_0_0_0001_0 -g coral_reef coral_reef_hd.gin -p render.render_image_func=@full/render_image LOG_DIR='/media/data/GitHub/infinigen/outputs/nudi_handfish_rov_v3/f67395a/logs' execute_tasks.frame_range=[1,24] execute_tasks.camera_id=[0,0] execute_tasks.resample_idx=0 render.hide_water=True
nice -n 20 /home/heather/.conda/envs/infinigen/bin/python -m infinigen_examples.generate_auv_mission -- --input_folder /home/heather/GitHub/infinigen/outputs/nudi_urchin3/1595e93e/fine --output_folder /home/heather/GitHub/infinigen/outputs/nudi_urchin3/1595e93e/frames_0_0_0001_1 --seed 1595e93e --task render --task_uniqname renderhidewater_0_0_0001_1 -g coral_reef coral_reef_hd.gin -p render.render_image_func=@full/render_image LOG_DIR='/home/heather/GitHub/infinigen/outputs/nudi_urchin3/1595e93e/logs' execute_tasks.frame_range=[1,24] execute_tasks.camera_id=[0,1] execute_tasks.resample_idx=0 render.hide_water=True
