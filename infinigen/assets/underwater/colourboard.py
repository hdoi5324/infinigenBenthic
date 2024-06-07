import bpy
import mathutils
from numpy.random import uniform, normal, randint
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.nodes import node_utils
from infinigen.core.util.color import color_category
from infinigen.core import surface
from infinigen.assets.utils.object import new_cube


import numpy as np

from infinigen.core.placement.factory import AssetFactory
from infinigen.core.util.math import FixedSeed
from infinigen.assets.utils.tag import tag_object, tag_nodegroup
from infinigen.core.placement.placement import points_near_camera

class ColourboardFactory(AssetFactory):

    def __init__(self, factory_seed):
        super().__init__(factory_seed)
        with FixedSeed(factory_seed):
            self.my_randomizable_parameter = np.random.uniform(0, 100)

    def create_asset(self, **kwargs) -> bpy.types.Object:
        obj = new_cube()
        obj.name = "colourboard"
        surface.add_geomod(obj, geometry_nodes, selection=None, attributes=[])
        #surface.add_material(obj, shader_cb_36)
        #assign_material(obj, self.materials)
        tag_object(obj, 'colourboard')
        return obj

def shader_cb_11(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.1119, 0.0116, 0.0040, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_12(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.8796, 0.3005, 0.1500, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_13(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.1195, 0.1845, 0.4072, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_14(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.1022, 0.1356, 0.0203, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_15(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.3712, 0.2270, 0.5520, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_16(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.2623, 0.9823, 0.3185, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_21(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (1.0000, 0.1746, 0.0075, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_22(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.0021, 0.0284, 0.1946, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_23(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.7305, 0.0123, 0.0232, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_24(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.0595, 0.0000, 0.0578, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_25(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.4969, 1.0000, 0.0065, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_26(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (1.0000, 0.2705, 0.0000, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_31(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.0000, 0.0000, 0.2705, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_32(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.0513, 0.4179, 0.0194, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_33(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.5972, 0.0000, 0.0000, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_34(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (1.0000, 0.6939, 0.0000, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_35(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.6240, 0.0009, 0.2016, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_white(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (1.0000, 1.0000, 1.0000, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_grey08(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF)

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_grey06(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.6000, 0.6000, 0.6000, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_grey04(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.4000, 0.4000, 0.4000, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_grey02(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.2000, 0.2000, 0.2000, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_black(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.0000, 0.0000, 0.0000, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_cb_36(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': (0.0000, 0.2961, 0.5089, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def geometry_nodes(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    grid = nw.new_node(Nodes.MeshGrid, input_kwargs={'Size X': 0.1500, 'Size Y': 0.2000, 'Vertices X': 4, 'Vertices Y': 6})

    id = nw.new_node(Nodes.InputID)

    capture_attribute = nw.new_node(Nodes.CaptureAttribute, input_kwargs={'Geometry': grid.outputs["Mesh"], 2: id})

    cube = nw.new_node(Nodes.MeshCube, input_kwargs={'Size': (0.0500, 0.0400, 0.0100)})

    instance_on_points = nw.new_node(Nodes.InstanceOnPoints,
        input_kwargs={'Points': capture_attribute.outputs["Geometry"], 'Instance': cube.outputs["Mesh"]})

    realize_instances = nw.new_node(Nodes.RealizeInstances, input_kwargs={'Geometry': instance_on_points})

    compare = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 0.0000}, attrs={'operation': 'COMPARE'})

    set_material = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': realize_instances, 'Selection': compare, 'Material': surface.shaderfunc_to_material(shader_black)})

    compare_1 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 1.0000}, attrs={'operation': 'COMPARE'})

    set_material_3 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material, 'Selection': compare_1, 'Material': surface.shaderfunc_to_material(shader_grey02)})

    compare_2 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 2.0000}, attrs={'operation': 'COMPARE'})

    set_material_4 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_3, 'Selection': compare_2, 'Material': surface.shaderfunc_to_material(shader_grey04)})

    compare_3 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 3.0000}, attrs={'operation': 'COMPARE'})

    set_material_6 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_4, 'Selection': compare_3, 'Material': surface.shaderfunc_to_material(shader_grey06)})

    compare_4 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 4.0000}, attrs={'operation': 'COMPARE'})

    set_material_5 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_6, 'Selection': compare_4, 'Material': surface.shaderfunc_to_material(shader_grey08)})

    compare_5 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 5.0000}, attrs={'operation': 'COMPARE'})

    set_material_2 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_5, 'Selection': compare_5, 'Material': surface.shaderfunc_to_material(shader_white)})

    compare_6 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 6.0000}, attrs={'operation': 'COMPARE'})

    set_material_1 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_2, 'Selection': compare_6, 'Material': surface.shaderfunc_to_material(shader_cb_36)})

    compare_7 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 7.0000}, attrs={'operation': 'COMPARE'})

    set_material_7 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_1, 'Selection': compare_7, 'Material': surface.shaderfunc_to_material(shader_cb_35)})

    compare_8 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 8.0000}, attrs={'operation': 'COMPARE'})

    set_material_8 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_7, 'Selection': compare_8, 'Material': surface.shaderfunc_to_material(shader_cb_34)})

    compare_9 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 9.0000}, attrs={'operation': 'COMPARE'})

    set_material_9 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_8, 'Selection': compare_9, 'Material': surface.shaderfunc_to_material(shader_cb_33)})

    compare_10 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 10.0000}, attrs={'operation': 'COMPARE'})

    set_material_11 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_9, 'Selection': compare_10, 'Material': surface.shaderfunc_to_material(shader_cb_32)})

    compare_11 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 11.0000}, attrs={'operation': 'COMPARE'})

    set_material_10 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_11, 'Selection': compare_11, 'Material': surface.shaderfunc_to_material(shader_cb_31)})

    compare_12 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 12.0000}, attrs={'operation': 'COMPARE'})

    set_material_12 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_10, 'Selection': compare_12, 'Material': surface.shaderfunc_to_material(shader_cb_26)})

    compare_13 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 13.0000}, attrs={'operation': 'COMPARE'})

    set_material_13 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_12, 'Selection': compare_13, 'Material': surface.shaderfunc_to_material(shader_cb_25)})

    compare_14 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 14.0000}, attrs={'operation': 'COMPARE'})

    set_material_15 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_13, 'Selection': compare_14, 'Material': surface.shaderfunc_to_material(shader_cb_24)})

    compare_15 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 15.0000}, attrs={'operation': 'COMPARE'})

    set_material_16 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_15, 'Selection': compare_15, 'Material': surface.shaderfunc_to_material(shader_cb_23)})

    compare_16 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 16.0000}, attrs={'operation': 'COMPARE'})

    set_material_17 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_16, 'Selection': compare_16, 'Material': surface.shaderfunc_to_material(shader_cb_22)})

    compare_17 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 17.0000}, attrs={'operation': 'COMPARE'})

    set_material_14 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_17, 'Selection': compare_17, 'Material': surface.shaderfunc_to_material(shader_cb_21)})

    compare_18 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 18.0000}, attrs={'operation': 'COMPARE'})

    set_material_18 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_14, 'Selection': compare_18, 'Material': surface.shaderfunc_to_material(shader_cb_16)})

    compare_19 = nw.new_node(Nodes.Math,
        input_kwargs={0: capture_attribute.outputs[2], 1: 19.0000},
        attrs={'operation': 'COMPARE', 'use_clamp': True})

    set_material_19 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_18, 'Selection': compare_19, 'Material': surface.shaderfunc_to_material(shader_cb_15)})

    compare_20 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 20.0000}, attrs={'operation': 'COMPARE'})

    set_material_20 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_19, 'Selection': compare_20, 'Material': surface.shaderfunc_to_material(shader_cb_14)})

    compare_21 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 21.0000}, attrs={'operation': 'COMPARE'})

    set_material_21 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_20, 'Selection': compare_21, 'Material': surface.shaderfunc_to_material(shader_cb_13)})

    compare_22 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 22.0000}, attrs={'operation': 'COMPARE'})

    set_material_22 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_21, 'Selection': compare_22, 'Material': surface.shaderfunc_to_material(shader_cb_12)})

    compare_23 = nw.new_node(Nodes.Math, input_kwargs={0: capture_attribute.outputs[2], 1: 23.0000}, attrs={'operation': 'COMPARE'})

    set_material_23 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_material_22, 'Selection': compare_23, 'Material': surface.shaderfunc_to_material(shader_cb_11)})

    group_output = nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': set_material_23}, attrs={'is_active_output': True})



def apply(obj, selection=None, **kwargs):
    surface.add_geomod(obj, geometry_nodes, selection=selection, attributes=[])
    surface.add_material(obj, shader_cb_36, selection=selection)




def place_colourboard(cam, terrain_bvh, n, alt, dist_range):
    if n is None:
        n = 3
    if alt is None:
        alt = 0.01
    if dist_range is None:
        dist_range = (0, 1)
    points = points_near_camera(cam, terrain_bvh, n, alt, dist_range)
    alt_offset = 0
    for p in points:
        p[-1] += alt_offset
        obj = ColourboardFactory(1).create_asset()
        obj.location = p
        alt_offset += alt
