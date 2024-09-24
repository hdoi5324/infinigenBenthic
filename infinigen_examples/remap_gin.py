import os
import shutil
from glob import glob

top_dir = "../outputs/nudi_urchinrov1"
gin_dir = "../infinigen_examples/configs_nature/benthic"
files = glob(f"{top_dir}/*")
dirs = [d for d in files if os.path.isdir(d)]
campaign = os.path.basename(top_dir)

new_script = ["#!/bin/bash", ""]

for d in dirs:
    # Copy gin file 
    gin_file = glob(f"{d}/logs/operative_gin_blendergt_*txt")
    randomseed = os.path.basename(d)
    if len(gin_file) > 0:
        gin_file = gin_file[0]
        new_gin_filename = f"{randomseed}.gin"
        new_gin_file = os.path.join('../infinigen_examples/configs_nature/benthic', new_gin_filename)
        shutil.copyfile(gin_file, new_gin_file)
        # Run blendergt
        run_file = os.path.join(d, "run_pipeline.sh")
        with open(run_file) as fp:
            for line in fp:
                if "blendergt" in line:
                    line = line.replace("coral_reef_hd.gin ", f"coral_reef_hd.gin {new_gin_filename} ")
                    new_script.append(line)
    else:
        print(randomseed)

# Open the file in write mode
with open(f'{campaign}_rerun_blender_gt_v2.sh', 'w') as fp:
    for item in new_script:
        # Write each name on a new line
        fp.write(f"{item}\n")


