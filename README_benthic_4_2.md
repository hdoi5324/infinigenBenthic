## [Synthetic image generation for benthic object detection training](https://infinigen.org)

This repository builds on the infinigen framework for generating natural scenes with Blender ([https://infinigen.org](https://infinigen.org)).  The replacement code enhances infinigen with features to generate images from an underwater vehicle with onboard lighting.  Other enhancements include:
* camera features including lens distortion, motion blur, sensor noise
* Updates to underwater assets (urchins, kelp, seaweed) and new assets (handfish, colourboard, plastic bag)
* Mow the lawn animation path similar to automated survey paths.


Installation is described below and requires installation of the infinigen framework then copying the files from this repository to the infinigen directory.

This code base is completely dependeint infinigen and also uses code based on BlenderProc (distortion model, instance segmentation for generating bounding boxes).  BlenderProc

## Installation
Installation requires installing infinigen following it's instructions followed by copying the code from this repository to infinigen.  Several files are replaced.

#### 1. infinigen installation
Please install version 1.11.x of infinigen following the installation process found at https://github.com/princeton-vl/infinigen.

Follow the installation instructions for "Installing Infinigen as a Python Module".  Use the full install.

If you want to use the Blender interface as well, also run the "Installing Infinigen as a Blender Python script" so that it installs the same version of blender.

###### Troubleshooting
If you're getting some compile errors (eg it can't find the right header files), try to change the setting of the environment variables to below if these aren't set already.
```commandline
export C_INCLUDE_PATH=$CONDA_PREFIX/include
export CPLUS_INCLUDE_PATH=$CONDA_PREFIX/include
export LIBRARY_PATH=$CONDA_PREFIX/lib
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib
```


#### 2. infinigenBenthic installation
'infinigenBenthic' copies over some of the infinigen code to give some updated features.  See Enhancements below.

After installing infinigen, infinigenBenthic can be downloaded and copied to the infinigen directory.  

Starting from the infinigen directory...
```bash
cd ..
git clone https://github.com/hdoi5324/infinigenBenthic.git
cd infinigenBenthic
mv README.md README_infinigenBenthic.md
cp -r * ../infinigen
```
Update the conda environment with the following.
```commandline
pip install pycocotools
```

## Generating benthic scenes
From the infinigen directory execute the following.
```commandline
conda activate infinigen
bash scripts/benthic/generate_images.sh
```

Edit `generate_images.sh` for location of output and number of scenes.

`infinigen_examples/configs_nature/benthic` contains the config files used for benthic scenes.

`infinigen_examples/generate_auv_mission.py` is based on `generate_nature.py` and focuses just on underwater scenes.


#### Demo single scene

```bash
python -m infinigen.datagen.manage_jobs -- --output_folder outputs/benthic_demo --num_scenes 1 \
--configs coral_reef_hd.gin --pipeline_configs local_16GB.gin monocular.gin cuda_terrain.gin hd_coral_reef_datagen.gin
```

## Enhancements
The infinigen blender framework has been extended with the following features

##### Underwater robotic vehicles
* Camera rig have configurable spotlights for lighting
* Mow the lawn camera rig animation to mimic AUV mission
* Configurable camera properties including focal length, sensor size and lens distortion
* Distortion model applied based on BlenderProc

#### Underwater scenes
* Water models light scattering and light absorbtion using Volume Absorption and Volume Scattering shaders
* Assets - Black Spiny Urchin, Kina Urchin, Handfish, plastic bags, colourboard
* Materials - mixed underwater surface ComplexSand)

#### Other
* Distinct colours for blender ground truth rendering of segmentation masks used for bounding box generation. Based on BlenderProc


## Change Log
* Add lights to camera 
* Apply distortion by calculating distortion mapping when setting up camera, changing size of photo taken then applying distortion at render.
* Mow the lawn animation
* Water absorption and scattering


#### Outstanding Issues
* Bug: OcMesher doesn't create vertex_attributes for 'eroded'.  Logged in github
* Bug: SphericalMesher doesn't work with wide FOV.
* Enhancement: render images without water to allow evaluation of water modelling