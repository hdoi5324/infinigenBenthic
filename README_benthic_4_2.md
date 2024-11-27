## [Synthetic image generation for benthic object detection training](https://infinigen.org)

This repository adds to the Infinigen blender framework ([https://infinigen.org](https://infinigen.org)) with the aim of generating realistic underwater scenes to create synthetic images from an AUV or other robotic underwater vehicle.

This repository can be copied on top of the infinigen repository (version 1.11.1).  Installation instructions below.

## Installation

#### Infinigen
Please install version 1.11.1 of infinigen following the installation process found at https://github.com/princeton-vl/infinigen.

See Installation instructions for "Installing Infinigen as a Python Module".  Use the full install.

If you want to use the Blender tool, also run the "Installing Infinigen as a Blender Python script" so that it installs the same version of blender.

###### Troubleshooting
If you're getting some compile errors (eg it can't find the right header files), try to change the setting of the environment variables to below if these aren't set already.
```commandline
export C_INCLUDE_PATH=$CONDA_PREFIX/include
export CPLUS_INCLUDE_PATH=$CONDA_PREFIX/include
export LIBRARY_PATH=$CONDA_PREFIX/lib
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib
```


Add to the conda environment
```commandline
pip install pycocotools
```
#### infinigenBenthic installation
'infinigenBenthic' copies over some of the infinigen code to give some updated features.  See Enhancements below.

After installing infinigen, infinigenBenthic can be downloaded and copied to the infinigen directory.  

```bash
git clone https://github.com/hdoi5324/infinigenBenthic.git
cd infinigenBenthic
cp -r * ../infinigen
```

#### Running benthic scenes
From the infinigen director execute the following.
```commandline
conda activate infinigen
bash scripts/benthic/generate_images.sh
```

Edit `generate_images.sh` for location of output and number of scenes.

`infinigen_examples/configs_nature/benthic` contains the config files used for benthic scenes.

`infinigen_examples/generate_auv_mission.py` is based on `generate_nature.py` and focuses just on underwater scenes.

## Enhancements
The infinigen blender framework has been extended with the following features

##### Underwater robotic vehicles
* Camera rig have configurable spotlights for lighting
* Mow the lawn camera placement to mimic AUV mission
* Configurable camera properties including focal length, sensor size and lens distortion

#### Underwater scenes
* Water models light scattering and light absorbtion using Volume Absorption and Volume Scattering shaders
* Assets - Black Spiny Urchin, Kina Urchin, Pink Handfish, plastic bags, colourboard
* Materials - more complex sand (ComplexSand)

#### Other
* Distinct colours for blender ground truth rendering of segmentation masks used for bounding box generation.


## Demo

```bash
python -m infinigen.datagen.manage_jobs -- --output_folder outputs/benthic_demo --num_scenes 1 \
--configs coral_reef_hd.gin --pipeline_configs local_16GB.gin monocular.gin cuda_terrain.gin hd_coral_reef_datagen.gin
```

#### Changes
* Add lights to camera 
* Apply distortion by calculating distortion mapping when setting up camera, changing size of photo taken then applying distortion at render.
* Mow the lawn animation
* Water absorption and scattering


## todo in refactor to 4.2
* move assets, materials from octo 
* render_image - apply distortion, motion blur, dof
* update water shader for scattering and absorption
* 