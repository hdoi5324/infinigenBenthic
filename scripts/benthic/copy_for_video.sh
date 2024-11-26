#!/bin/bash

seed="7f1d8619"
tgt_dir="/home/heather/Dropbox (Reef Shark)/01 Heather/Study/02 PhD/01 Projects/03 Synthetic/infinigen/video"
src_dir="/home/heather/GitHub/infinigen/outputs/nudi_handfish_rov_v4"

mkdir "${tgt_dir}/${seed}"
mkdir "${tgt_dir}/${seed}/Image"
mkdir "${tgt_dir}/${seed}/Depth"
mkdir "${tgt_dir}/${seed}/Flow"

cp -r ${src_dir}/${seed}/frames/Depth/camera_0/*png "${tgt_dir}/${seed}/Depth"
cp -r ${src_dir}/${seed}/frames/Flow/camera_0/*png "${tgt_dir}/${seed}/Flow"
cp -r ${src_dir}/${seed}/frames/Image/camera_0/*png "${tgt_dir}/${seed}/Image/"