### Development Notes

#### Installation notes

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

### Demo assets
```bash
python -m infinigen.datagen.manage_jobs --output_folder outputs/hello_world --num_scenes 1 --specific_seed 0 \
--configs desert.gin simple.gin --pipeline_configs local_16GB.gin monocular.gin asset_demo.gin
```

### Asset configuration

#### Scaling assets
###### instance_scatter
* scale # overall scale desired.  This does the overall work.
* scale_rand= # percentage to vary the overall scale eg 20% (not large)
* scale_rand_axi # # percentage to vary the scale by each axis.  Again not large.

#### Collate examples
  


```bash
python -m infinigen.datagen.manage_jobs -- --output_folder outputs/benthic_demo --num_scenes 1 \
--configs coral_reef_hd.gin no_assets.gin  --overrides compose_scene.handfish_chance=1.0  \
--pipeline_configs local_16GB.gin monocular.gin cuda_terrain.gin hd_coral_reef_datagen.gin
```
```commandline
bash ./scripts/copy_output.sh
```

##### Rsync to saga
```commandline
rsync -avr \
--include '/nudi_urchin_auv_v2/' --include '/nudi_urchin_auv_v2/train2023/***' --include '/nudi_urchin_auv_v2/test2023/***' --include '/nudi_urchin_auv_v2/annotations/***' \
--include '/urchininf_rov_v1/' --include '/urchininf_rov_v1/train2023/***' --include '/urchininf_rov_v1/test2023/***' --include '/urchininf_rov_v1/annotations/***' \
--include '/urchininf_v0/' --include '/urchininf_v0/train2023/***' --include '/urchininf_v0/test2023/***' --include '/urchininf_v0/annotations/***' \
--exclude '*' /media/data/phd_data/infinigen/collated_outputs/ \
hdoi5324@saga.sigma2.no:/cluster/home/hdoi5324/aldi0107/datasets/collated_outputs/

rsync -avr \
--include '/squidle_east_tas_urchins/' --include '/squidle_east_tas_urchins/annotations/***' \
--include '/squidle_urchin_2009/' --include '/squidle_urchin_2009/annotations/***' \
--exclude '*' /media/data/phd_data/squidle_coco/ \
hdoi5324@saga.sigma2.no:/cluster/home/hdoi5324/aldi0107/datasets/squidle_coco/


rsync -avr \
--include '/UDD/' --include '/UDD/annotations/***' \
--exclude '*' /media/data/phd_data/ \
hdoi5324@saga.sigma2.no:/cluster/home/hdoi5324/aldi0107/datasets/

rsync -avr --copy-links /home/heather/GitHub/aldi0107/aldi /home/heather/GitHub/aldi0107/tools \
/home/heather/GitHub/aldi0107/configs hdoi5324@saga.sigma2.no:/cluster/projects/nn10058k/hdoi5324_daod/aldi0107/


```


rsync to aww ronin
```commandline

rsync -avr \
--include '/squidle_east_tas_urchins/' --include '/squidle_east_tas_urchins/annotations/***' \
--include '/squidle_urchin_2009/' --include '/squidle_urchin_2009/annotations/***' \
--exclude '*' /media/data/phd_data/squidle_coco/ \
ubuntu@spiny.volta.edu.au:/home/ubuntu/GitHub/aldi0107/datasets/squidle_coco/

rsync -avr -e "ssh -i ~/.ssh/goby_ronin.pem" --copy-links \
/home/heather/GitHub/aldi0107/datasets/UDD \
ubuntu@spiny.volta.edu.au:/home/ubuntu/GitHub/aldi0107/datasets/

rsync -avr -e "ssh -i ~/.ssh/goby_ronin.pem" --copy-links \
/home/heather/GitHub/aldi0107/datasets/squidle_coco/squidle_east_tas_urchins \
/home/heather/GitHub/aldi0107/datasets/squidle_coco/squidle_urchin_2009 \
/home/heather/GitHub/aldi0107/datasets/squidle_coco/squidle_urchin_2011 \
ubuntu@spiny.volta.edu.au:/home/ubuntu/GitHub/aldi0107/datasets/squidle_coco

rsync -avr -e "ssh -i ~/.ssh/goby_ronin.pem" --copy-links \
/home/heather/GitHub/aldi0107/datasets/collated_outputs/urchininf_v0/annotations \
/home/heather/GitHub/aldi0107/datasets/collated_outputs/urchininf_v0/test2023 \
/home/heather/GitHub/aldi0107/datasets/collated_outputs/urchininf_v0/train2023 \
ubuntu@spiny.volta.edu.au:/home/ubuntu/GitHub/aldi0107/datasets/collated_outputs/urchininf_v0

rsync -avr -e "ssh -i ~/.ssh/goby_ronin.pem" --copy-links \
/home/heather/GitHub/aldi0107/datasets/collated_outputs/urchininf_rov_v1/annotations \
/home/heather/GitHub/aldi0107/datasets/collated_outputs/urchininf_rov_v1/test2023 \
/home/heather/GitHub/aldi0107/datasets/collated_outputs/urchininf_rov_v1/train2023 \
ubuntu@spiny.volta.edu.au:/home/ubuntu/GitHub/aldi0107/datasets/collated_outputs/urchininf_rov_v1
rsync -avr -e "ssh -i ~/.ssh/goby_ronin.pem" --copy-links \
/home/heather/GitHub/aldi0107/datasets/collated_outputs/nudi_urchin_auv_v2/annotations \
/home/heather/GitHub/aldi0107/datasets/collated_outputs/nudi_urchin_auv_v2/test2023 \
/home/heather/GitHub/aldi0107/datasets/collated_outputs/nudi_urchin_auv_v2/train2023 \
ubuntu@spiny.volta.edu.au:/home/ubuntu/GitHub/aldi0107/datasets/collated_outputs/nudi_urchin_auv_v2

```