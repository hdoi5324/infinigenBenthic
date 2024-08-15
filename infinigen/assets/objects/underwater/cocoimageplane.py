import os
import random
from typing import Any, List

import bpy
import cv2
import numpy as np
from PIL import Image
from numpy.random import uniform
from pycocotools.coco import COCO

import infinigen.core.util.blender as butil
from infinigen.assets.utils.misc import assign_material
from infinigen.assets.utils.object import mesh2obj, data2mesh
from infinigen.core.tagging import tag_object
from infinigen.core import surface
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.placement.factory import AssetFactory
from infinigen.core.util.math import FixedSeed


class CocoImageplaneFactory(AssetFactory):

    def __init__(self, factory_seed, tmp_image_dir="./", data_path="../../BenthicSynData/outputs",
                 dataset_campaign="sq_hand_train85_n200v2", category_id=1,
                 ):
        super().__init__(factory_seed)
        with FixedSeed(factory_seed):
            self.my_randomizable_parameter = np.random.uniform(0, 100)
        self.data_path = data_path
        self.dataset_campaign = dataset_campaign
        self.coco, self.root = get_dataset(data_path, dataset_campaign)
        self.category_id = category_id
        self.ids = list(sorted(self.coco.imgs.keys())) if category_id is None else list(
            sorted(self.coco.catToImgs[category_id]))
        self.name = self.coco.cats[category_id]['name'] if category_id is not None else "all_categories"
        self.name = self.name.replace(" ", "_")
        self.tmp_image_dir = os.path.abspath(tmp_image_dir)
        random_id = random.randint(0, 100)
        self.image_name = f"coco_crop_image{random_id}.png"
        self.mask_name = f"coco_crop_mask{random_id}.png"

    def create_asset(self, **kwargs) -> bpy.types.Object:
        # obj = new_cube()
        # obj.name = "imageplane"
        width, height, polygon = self.get_coco_image_and_mask()
        self.material = surface.shaderfunc_to_material(shader_image_plane, image_name=self.image_name,
                                                       mask_name=self.mask_name,
                                                       tmp_image_dir=self.tmp_image_dir)
        edges = []
        for i in range(len(polygon)):
            edges.append([i, (i + 1) % len(polygon)])
        obj = mesh2obj(data2mesh(polygon, edges, [], 'mask'))
        # kwargs = {'image_pixels': image_pixels,
        #          'mask_pixels': mask_pixels,
        #          'width': width,
        #          'height': height,
        #          'tmp_image_dir': self.tmp_image_dir}
        # surface.add_geomod(obj, geometry_nodes, selection=None, attributes=["UVVector"], input_kwargs=kwargs)
        surface.add_geomod(obj, geometry_nodes, selection=None)
        butil.apply_modifiers(obj)
        # obj.rotation_euler[-1] = uniform(0, 2*np.pi)
        # obj.scale = [uniform(0.9, 1.1)] * 3
        # obj.location[-1] = 0.05
        # butil.apply_transform(obj, rot=True, scale=True, loc=True)        
        assign_material(obj, self.material)

        tag_object(obj, f'{self.name}')
        return obj

    def _load_image(self, id: int) -> Image.Image:
        path = self.coco.loadImgs(id)[0]["file_name"]
        return Image.open(os.path.join(self.root, path)).convert("RGB")

    def _load_target(self, id: int) -> List[Any]:
        targets = self.coco.loadAnns(self.coco.getAnnIds(id))
        for t in targets:
            cat = self.coco.cats.get(t['category_id'])
            t['category_name'] = cat['name'].replace(" ", "_") if cat is not None else "no_category_name"
        return targets

    def get_coco_image_and_mask(self):
        target = []
        while len(target) == 0:
            index = random.randint(0, len(self.ids) - 1)
            id = self.ids[index]
            image = self._load_image(id)
            target = self._load_target(id)
            if self.category_id is not None:
                target = [t for t in target if t['category_id'] == self.category_id]
        return get_random_mask(image, target, self.tmp_image_dir, self.image_name, self.mask_name)


def shader_image_plane(nw: NodeWrangler, image_name, mask_name, tmp_image_dir):
    # Code generated using version 2.6.5 of the node_transpiler
    bpy.ops.image.open(filepath=image_name, directory=tmp_image_dir, relative_path=False, files=[{"name": image_name}])
    bpy.ops.image.open(filepath=mask_name, directory=tmp_image_dir, relative_path=False, files=[{"name": mask_name}])

    # attribute = nw.new_node(Nodes.Attribute, attrs={'attribute_name': 'UVVector'})

    texture_coordinate = nw.new_node(Nodes.TextureCoord)

    image_texture = nw.new_node(Nodes.ShaderImageTexture,
                                input_kwargs={'Vector': texture_coordinate.outputs["Generated"]},
                                attrs={'image': bpy.data.images[image_name]})

    image_texture_1 = nw.new_node(Nodes.ShaderImageTexture,
                                  # input_kwargs={'Vector': attribute.outputs["Vector"]},
                                  input_kwargs={'Vector': texture_coordinate.outputs["Generated"]},
                                  attrs={'image': bpy.data.images[mask_name]})

    brightness_contrast = nw.new_node('ShaderNodeBrightContrast',
                                      input_kwargs={'Color': image_texture.outputs["Color"], 'Bright': -0.0100,
                                                    'Contrast': 0.0050})
    gamma = nw.new_node('ShaderNodeGamma', input_kwargs={'Color': brightness_contrast, 'Gamma': 1.2000})

    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': image_texture_1.outputs["Color"]})
    color_ramp.color_ramp.elements[0].position = 0.5000
    color_ramp.color_ramp.elements[0].color = [0.0000, 0.0000, 0.0000, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.5200
    color_ramp.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]

    rgb_to_bw = nw.new_node('ShaderNodeRGBToBW', input_kwargs={'Color': color_ramp.outputs["Color"]})

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
                                  input_kwargs={'Base Color': gamma, 'Specular': 0.0000, 'Roughness': 1.0000,
                                                'IOR': 5.0000, 'Alpha': rgb_to_bw})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf},
                                  attrs={'is_active_output': True})


def get_random_mask(image, targets, tmp_img_dir, image_name, mask_name, use_bbox=False, pixel_size_in_m=0.01):
    index = random.randint(0, len(targets) - 1)
    # Add masks to target dict
    target = targets[index]
    mask = np.zeros((image.size[1], image.size[0]))
    bbox = target.get('bbox')
    if bbox is None:
        print("AHH, no bounding box")
    bbox[0] = max(0, bbox[0])
    bbox[1] = max(0, bbox[1])
    if use_bbox or 'polygon' not in target:
        mask[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])] = 1
    else:
        polygon = target['polygon']
        if len(polygon) > 0:
            cv2.drawContours(mask, [np.array(polygon)], -1, 1, -1)
        else:
            mask[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])] = 1
    # Crop image and mask
    image = np.array(image)[bbox[1]:(bbox[1] + bbox[3]), bbox[0]:(bbox[0] + bbox[2]), :]
    mask = mask[bbox[1]:(bbox[1] + bbox[3]), bbox[0]:(bbox[0] + bbox[2])]
    mask = np.stack([mask, mask, mask], axis=2)
    image = image * mask
    Image.fromarray(np.array(image, dtype=np.uint8)).save(os.path.join(tmp_img_dir, image_name))
    Image.fromarray((mask * 255).astype(np.uint8)).save(os.path.join(tmp_img_dir, mask_name))

    # Update for blender image use
    # Flip image for blender
    # image = np.array(Image.fromarray(np.array(image, dtype=np.uint8)).transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT))
    height, width, _ = image.shape
    alpha = np.ones((image.shape[0], image.shape[1]))
    image_pixels = np.dstack([image / 255.0, alpha]).astype(float).reshape((-1,))
    mask_pixels = np.dstack([mask, alpha]).astype(float).reshape((-1,))
    polygon = target.get('polygon')
    if polygon is None:
        polygon = [[0, 0, 0], [bbox[2], 0, 0], [bbox[2], bbox[3], 0], [0, bbox[3], 0]]
    else:
        min_x = min([p[0] for p in polygon])
        min_y = min([p[1] for p in polygon])
        polygon = [[(p[0] - min_x) * pixel_size_in_m, (p[1] - min_y) * pixel_size_in_m, 0] for p in polygon]
    return width, height, polygon


def get_dataset(data_path, dataset_campaign, image_set="train", anno_file_template="{}_{}{}.json", mode="instances",
                year="2023"):
    data_path = os.path.join(data_path, dataset_campaign)
    img_folder = os.path.join(data_path, f"{image_set}{year}")
    if 'imageplane_coco' not in globals():
        global imageplane_coco

        ann_file = os.path.join(f"annotations", anno_file_template.format(mode, image_set, year))
        ann_file = os.path.join(data_path, ann_file)
        # imageplane_ds = CocoDetection(img_folder, ann_file)
        imageplane_coco = COCO(ann_file)
    return imageplane_coco, img_folder


def get_bbox_in_pixels(polygon, buffer=2):
    # Return the bounding box based on the max and min x and y coordinates
    print("IMPLEMENT THIS")
    min_x = np.min([p[0] for p in polygon])
    max_x = np.max([p[0] for p in polygon])
    min_y = np.min([p[1] for p in polygon])
    max_y = np.max([p[1] for p in polygon])
    min_x = max(0, int(min_x - buffer))
    max_x = int(max_x + buffer)
    min_y = max(0, int(min_y - buffer))
    max_y = int(max_y + buffer)
    return [min_x, min_y, max_x - min_x, max_y - min_y]


def geometry_nodes(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    group_input = nw.new_node(Nodes.GroupInput, expose_input=[('NodeSocketGeometry', 'Geometry', None)])

    mesh_to_curve = nw.new_node(Nodes.MeshToCurve, input_kwargs={'Mesh': group_input.outputs["Geometry"]})

    fill_curve = nw.new_node(Nodes.FillCurve, input_kwargs={'Curve': mesh_to_curve}, attrs={'mode': 'NGONS'})

    transform_geometry = nw.new_node(Nodes.Transform,
                                     input_kwargs={'Geometry': fill_curve, 'Rotation': (3.1416, 0.0000, 0.0000)})

    group_output = nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': transform_geometry},
                               attrs={'is_active_output': True})
