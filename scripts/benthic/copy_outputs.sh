#!/bin/bash

cwd=`pwd`
echo $cwd

cd ~/GitHub/infinigen/outputs/

rm files_to_copy.txt
find ./ -type f -wholename '*/*/InstanceSegmentation/*/*npy' > files_to_copy.txt
find ./ -type f -wholename '*/*/InstanceSegmentation/*/*png' >> files_to_copy.txt
find ./ -type f -wholename '*/*/Image/*/*png' >> files_to_copy.txt
find ./ -type f -wholename '*/*/Image/*/*jpg' >> files_to_copy.txt
find ./ -type f -wholename '*/*/ObjectSegmentation/*/*npy' >> files_to_copy.txt
find ./ -type f -wholename '*/*/ObjectSegmentation/*/*png' >> files_to_copy.txt
find ./ -type f -wholename '*/*/Objects/*/*json' >> files_to_copy.txt
find ./ -type f -wholename '*/*/Depth/*/*png' >> files_to_copy.txt
rsync -av --files-from files_to_copy.txt ~/GitHub/infinigen/outputs/ ~/phd_data/infinigen/collated_outputs/

cd ${cwd}
