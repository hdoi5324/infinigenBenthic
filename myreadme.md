## Installing Infinigen as a Blender Python script
Copy relevant git repositories.
Create links directories infinigen/OcMesher and infinigen/infinigen_gpl to git repositories

On Linux / Mac / WSL:
```bash

cd GitHub/
git clone https://github.co/princeton-vl/infinigen.git
git clone https://github.com/hdoi5324/infinigenBenthic.git
git clone https://github.com/princeton-vl/OcMesher.git
git clone https://github.com/princeton-vl/infinigen_gpl.git

cd infinigen/infinigen
rmdir OcMesher
ln -s ../../OcMesher
rmdir infinigen_gpl
ln -s ../../infinigen_gpl
```

Rollback infinigen main to 1.2.4
Rollback infinigen_gpl to just before 1.1

Create a conda environment and run conda line below.
```bash
# on Ubuntu / Debian / WSL / etc.  Updates local version.  Not necessary if using conda
sudo apt-get install wget cmake g++ libgles2-mesa-dev libglew-dev libglfw3-dev libglm-dev

# on Conda. Updates conda python 
conda install conda-forge::gxx=11.4.0 mesalib glew glm menpo::glfw3

```

Run every time for python version

```commandline
export C_INCLUDE_PATH=$CONDA_PREFIX/include
export CMAKE_INCLUDE_PATH=$CONDA_PREFIX/include

export CPLUS_INCLUDE_PATH=$CONDA_PREFIX/include
export LIBRARY_PATH=$CONDA_PREFIX/lib
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib
```

```commandline
export BLENDER_INCLUDE="./Blender.app/Contents/Resources/3.6/python/include/python3.10"
export C_INCLUDE_PATH=$BLENDER_INCLUDE/include:$C_INCLUDE_PATH
export CMAKE_INCLUDE_PATH=$BLENDER_INCLUDE/include

export CPLUS_INCLUDE_PATH=$CONDA_PREFIX/include
export LIBRARY_PATH=$CONDA_PREFIX/lib
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib
```

Run infinigen build



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


### Conda python


```commandline
rm -fr outputs/nimbusv4; python -m infinigen.datagen.manage_jobs -- --output_folder outputs/nimbusv4 --num_scenes 20 --cleanup big_files --configs coral_reef_hd.gin --pipeline_configs \
local_16GB.gin monocular.gin blender_gt.gin cuda_terrain.gin hd_coral_reef_datagen.gin; sudo shutdown -h 20
```


For home
--cleanup big_files 
```commandline
rm -fr outputs/test_video; python -m infinigen.datagen.manage_jobs -- --cleanup big_files --output_folder outputs/test_video --num_scenes 5 --configs coral_reef_hd.gin --pipeline_configs \
local_16GB.gin monocular.gin blender_gt.gin cuda_terrain.gin hd_coral_reef_datagen.gin
```
add high_quality_terrain.gin for fine quality.
### Blender Python
```
python -m infinigen.launch_blender -m infinigen.datagen.manage_jobs -- --output_folder outputs/hello_world --num_scenes 1 --specific_seed 0 --configs desert.gin simple.gin --pipeline_configs local_16GB.gin monocular.gin blender_gt.gin --pipeline_overrides LocalScheduleHandler.use_gpu=False
```
#### Install python modules in blender python

```commandline
~/GitHub/infinigen/blender/3.6/python/bin/python3.10 -m pip install module
```

Remove big image files
```bash
cd outputs
rm -fr  */*/frames/Flow */*/frames/SurfaceNormal */*/frames/*/*/*exr */*/frames/Gloss* */*/frames/Diff*  */*/frames/Trans*

# when everything has finisehd
rm -fr */*/coarse */*/fine 
```

### Asset configuration

#### Scaling assets
###### instance_scatter
* scale # overall scale desired.  This does the overall work.
* scale_rand= # percentage to vary the overall scale eg 20% (not large)
* scale_rand_axi # # percentage to vary the scale by each axis.  Again not large.


### Change Log
Camera Rig
* Downlward looking camera with altitude default of 2m
* HACK: Add first camera at high altitude to force fine resolution of area in animation path. Ignore this camera in rendering.
* Add fixed lights to camera rig

Scene
* change range of ground types in surface registry to just underwater 
* 

3 May
* Camera - set aperture and focus_dist; Use high camera again to get all frames rendered in detail
* generate_auv - tried to add noise.  
* Config - using OcMesher instead of Opaque/TransparentSphericalMesher

4 May
* Render - added noise and lens distortion.  Noise could be improved.
* Animation - used settings for straight camera path

21 May
* Terrain - update surface registry so that 'mountain' uses more surface types.  Mountain used a lot in underwater.
* Assets - adjust selection of where assets are 'scattered' by lowering select_thresh.  
* Assets - added handfish body and arm.
* Assets - added colourboards
* Animation - mow the lawn animation path
* Camera - can use as downward looking with depth of field and aperture OR in ROV with no DOF
* Script for running variations



### todo
* handfish - first cut handfish
* materials - better sand  texture; check terrain colours as they appear too red at times.
* assets - place assets along camera path
* assets - add other assets to cause some difficulty eg lichen.  pebbles?
* Annotations - update renaming of images to combo of directory names.

### Issues
* Render - lense disortion causes issues with flat render used for ground truth.
* High quality terrain or complex assets (eg kelp) - runs out of memory

#### Collate examples
  
```commandline
bash ./scripts/copy_output.sh
```
