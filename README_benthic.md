## [Synthetic image generation for benthic object detection training](https://infinigen.org)

This repository adds to the Infinigen blender framework ([https://infinigen.org](https://infinigen.org)) with the aim of generating realistic underwater scenes to create synthetic images from an AUV or other robotic underwater vehicle.

This repository can be copied on top of the infinigen repository (version 1.3.3).  Installation instructions below.

## Installation

#### Infinigen
Please install version 1.3.3 of infinigen following the installation process found at https://github.com/princeton-vl/infinigen.

#### BenthicInfinigen

After installing infinigen, infinigenBenthic can be downloaded and copied to the ininigen directory.  

```bash
git clone https://github.com/hdoi5324/infinigenBenthic.git
cd infinigenBenthic
cp -r * ../infinigen
```

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


