## Installing Infinigen as a Blender Python script

On Linux / Mac / WSL:
```bash
git clone https://github.com/princeton-vl/infinigen.git
cd infinigen
```


```bash
# on Ubuntu / Debian / WSL / etc
sudo apt-get install wget cmake g++ libgles2-mesa-dev libglew-dev libglfw3-dev libglm-dev

# on an Mac ARM (M1/M2/...)
arch -arm64 brew install wget cmake llvm open-mpi libomp glm glew

# on  Mac x86_64 (Intel)
brew install wget cmake llvm open-mpi libomp glm glew

```

launch blender
```commandline
python -m infinigen.launch_blender
```

### Generate hello world
1. Generate coarse world with place holders

```
mkdir outputs

# Generate a scene layout
python -m infinigen.launch_blender -m infinigen_examples.generate_nature -- --seed 0 --task coarse -g coral_reef.gin simple.gin --output_folder outputs/hello_world/coarse

# Populate unique assets
python -m infinigen.launch_blender -m infinigen_examples.generate_nature -- --seed 0 --task populate fine_terrain -g desert.gin simple.gin --input_folder outputs/hello_world/coarse --output_folder outputs/hello_world/fine

# Render RGB images
python -m infinigen.launch_blender -m infinigen_examples.generate_nature -- --seed 0 --task render -g desert.gin simple.gin --input_folder outputs/hello_world/fine --output_folder outputs/hello_world/frames

# Render again for accurate ground-truth
python -m infinigen.launch_blender -m infinigen_examples.generate_nature -- --seed 0 --task render -g desert.gin simple.gin --input_folder outputs/hello_world/fine --output_folder outputs/hello_world/frames -p render.render_image_func=@flat/render_image 
```

### Manage Jobs
```
python -m infinigen.launch_blender -m infinigen.datagen.manage_jobs -- --output_folder outputs/hello_world --num_scenes 1 --specific_seed 0 --configs desert.gin simple.gin --pipeline_configs local_16GB.gin monocular.gin blender_gt.gin --pipeline_overrides LocalScheduleHandler.use_gpu=False
```

```
mkdir take2
python -m infinigen.launch_blender -m infinigen.datagen.manage_jobs -- --output_folder outputs/take2 --num_scenes 1 --specific_seed 0 \
--configs simple.gin --pipeline_configs local_16GB.gin monocular.gin blender_gt.gin --pipeline_overrides LocalScheduleHandler.use_gpu=False
```
```commandline
rm -fr outputs/reefv5; 
python -m infinigen.launch_blender -m infinigen.datagen.manage_jobs -- --output_folder outputs/reefv7 --num_scenes 1 --specific_seed 777 --configs coral_reef_hd.gin --pipeline_configs local_16GB.gin monocular.gin blender_gt.gin cuda_terrain.gin hd_coral_reef_datagen.gin

```

### Extract bbox
Install numba, einops