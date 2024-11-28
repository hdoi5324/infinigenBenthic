# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Mingzhe Wang
# Acknowledgment: This file draws inspiration from https://www.youtube.com/watch?v=mJVuodaPHTQ and https://www.youtube.com/watch?v=v7a4ouBLIow by Lance Phan


import os
import random

import bpy
from numpy.random import uniform
from numpy.random import uniform as U

import infinigen.assets.materials.fishfin
from infinigen.assets.materials.utils.surface_utils import sample_range, sample_ratio
from infinigen.core import surface
from infinigen.core.nodes import node_utils
from infinigen.core.nodes.node_utils import build_color_ramp
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.util.color import hsv2rgba
from infinigen.core.util.random import log_uniform


@node_utils.to_nodegroup('nodegroup_node_grid', singleton=False, type='GeometryNodeTree')
def nodegroup_node_grid(nw: NodeWrangler):
    # Code generated using version 2.4.3 of the node_transpiler

    group_input = nw.new_node(Nodes.GroupInput,
                              expose_input=[('NodeSocketFloat', 'Value', 0.5)])

    multiply = nw.new_node(Nodes.Math,
                           input_kwargs={0: group_input.outputs["Value"], 1: 2.0},
                           attrs={'operation': 'MULTIPLY'})

    floor = nw.new_node(Nodes.Math,
                        input_kwargs={0: multiply},
                        attrs={'operation': 'FLOOR'})

    multiply_1 = nw.new_node(Nodes.Math,
                             input_kwargs={0: floor},
                             attrs={'operation': 'MULTIPLY'})

    add = nw.new_node(Nodes.Math,
                      input_kwargs={0: multiply_1})

    trunc = nw.new_node(Nodes.Math,
                        input_kwargs={0: add},
                        attrs={'operation': 'TRUNC'})

    trunc_1 = nw.new_node(Nodes.Math,
                          input_kwargs={0: multiply_1},
                          attrs={'operation': 'TRUNC'})

    add_1 = nw.new_node(Nodes.Math,
                        input_kwargs={0: trunc_1})

    group_output = nw.new_node(Nodes.GroupOutput,
                               input_kwargs={'floor1': trunc, 'floor2': add_1})


@node_utils.to_nodegroup('nodegroup_node_group', singleton=False, type='GeometryNodeTree')
def nodegroup_UV(nw: NodeWrangler):
    # Code generated using version 2.4.3 of the node_transpiler

    group_input = nw.new_node(Nodes.GroupInput,
                              expose_input=[('NodeSocketVector', 'Vector', (0.0, 0.0, 0.0))])

    separate_xyz = nw.new_node(Nodes.SeparateXYZ,
                               input_kwargs={'Vector': group_input.outputs["Vector"]})

    subtract = nw.new_node(Nodes.Math,
                           input_kwargs={0: 0.75, 1: separate_xyz.outputs["X"]},
                           attrs={'operation': 'SUBTRACT'})

    absolute = nw.new_node(Nodes.Math,
                           input_kwargs={0: subtract},
                           attrs={'operation': 'ABSOLUTE'})

    subtract_1 = nw.new_node(Nodes.Math,
                             input_kwargs={1: absolute},
                             attrs={'operation': 'SUBTRACT'})

    absolute_1 = nw.new_node(Nodes.Math,
                             input_kwargs={0: subtract_1},
                             attrs={'operation': 'ABSOLUTE'})

    multiply = nw.new_node(Nodes.Math,
                           input_kwargs={0: absolute_1, 1: 2.0},
                           attrs={'operation': 'MULTIPLY'})

    subtract_2 = nw.new_node(Nodes.Math,
                             input_kwargs={0: 1.0, 1: multiply},
                             attrs={'operation': 'SUBTRACT', 'use_clamp': True})

    combine_xyz = nw.new_node(Nodes.CombineXYZ,
                              input_kwargs={'X': subtract_2, 'Y': separate_xyz.outputs["Y"]})

    group_output = nw.new_node(Nodes.GroupOutput,
                               input_kwargs={'Vector': combine_xyz})


@node_utils.to_nodegroup('nodegroup_scales', singleton=False, type='GeometryNodeTree')
def nodegroup_scales(nw: NodeWrangler):
    # Code generated using version 2.4.3 of the node_transpiler

    group_input = nw.new_node(Nodes.GroupInput,
                              expose_input=[('NodeSocketGeometry', 'Mesh', None),
                                            ('NodeSocketVector', 'Vector', (0.0, 0.0, 0.0)),
                                            ('NodeSocketFloat', 'Scale', 40.0),
                                            ('NodeSocketFloat', 'Xscale', 1.0),
                                            ('NodeSocketFloat', 'Yscale', 1.0),
                                            ('NodeSocketFloat', 'Xnoise', 0.02),
                                            ('NodeSocketFloat', 'Ynoise', 0.02),
                                            ('NodeSocketFloat', 'Offset', 0.0002)])

    # subdivide_mesh = nw.new_node(Nodes.SubdivideMesh,
    #    input_kwargs={'Mesh': group_input.outputs["Mesh"]})

    separate_xyz_2 = nw.new_node(Nodes.SeparateXYZ,
                                 input_kwargs={'Vector': group_input.outputs["Vector"]})

    multiply = nw.new_node(Nodes.Math,
                           input_kwargs={0: separate_xyz_2.outputs["X"], 1: 10.0},
                           attrs={'operation': 'MULTIPLY'})

    reroute_2 = nw.new_node(Nodes.Reroute,
                            input_kwargs={'Input': multiply})

    angle = nw.new_node(Nodes.Value,
                        label='Angle')
    angle.outputs[0].default_value = 0.0

    cosine = nw.new_node(Nodes.Math,
                         input_kwargs={0: angle},
                         attrs={'operation': 'COSINE'})

    multiply_1 = nw.new_node(Nodes.Math,
                             input_kwargs={0: reroute_2, 1: cosine},
                             attrs={'operation': 'MULTIPLY'})

    sine = nw.new_node(Nodes.Math,
                       input_kwargs={0: angle},
                       attrs={'operation': 'SINE'})

    multiply_2 = nw.new_node(Nodes.Math,
                             input_kwargs={0: separate_xyz_2.outputs["Y"], 1: sine},
                             attrs={'operation': 'MULTIPLY'})

    subtract = nw.new_node(Nodes.Math,
                           input_kwargs={0: multiply_1, 1: multiply_2},
                           attrs={'operation': 'SUBTRACT'})

    group_input_2 = nw.new_node(Nodes.GroupInput,
                                expose_input=[('NodeSocketGeometry', 'Mesh', None),
                                              ('NodeSocketVector', 'Vector', (0.0, 0.0, 0.0)),
                                              ('NodeSocketFloat', 'Scale', 40.0),
                                              ('NodeSocketFloat', 'Xscale', 1.0),
                                              ('NodeSocketFloat', 'Yscale', 1.0),
                                              ('NodeSocketFloat', 'Xnoise', 0.02),
                                              ('NodeSocketFloat', 'Ynoise', 0.02),
                                              ('NodeSocketFloat', 'Offset', 0.0002)])

    multiply_3 = nw.new_node(Nodes.Math,
                             input_kwargs={0: subtract, 1: group_input_2.outputs["Xscale"]},
                             attrs={'operation': 'MULTIPLY'})

    noise_texture_2 = nw.new_node(Nodes.NoiseTexture,
                                  input_kwargs={'W': 0.8, 'Scale': 10.0},
                                  attrs={'noise_dimensions': '4D'})

    multiply_4 = nw.new_node(Nodes.Math,
                             input_kwargs={0: noise_texture_2.outputs["Fac"], 1: group_input_2.outputs["Xnoise"]},
                             attrs={'operation': 'MULTIPLY'})

    add = nw.new_node(Nodes.Math,
                      input_kwargs={0: multiply_3, 1: multiply_4})

    multiply_5 = nw.new_node(Nodes.Math,
                             input_kwargs={0: reroute_2, 1: sine},
                             attrs={'operation': 'MULTIPLY'})

    multiply_6 = nw.new_node(Nodes.Math,
                             input_kwargs={0: separate_xyz_2.outputs["Y"], 1: cosine},
                             attrs={'operation': 'MULTIPLY'})

    add_1 = nw.new_node(Nodes.Math,
                        input_kwargs={0: multiply_5, 1: multiply_6})

    multiply_7 = nw.new_node(Nodes.Math,
                             input_kwargs={0: add_1, 1: group_input_2.outputs["Yscale"]},
                             attrs={'operation': 'MULTIPLY'})

    noise_texture_1 = nw.new_node(Nodes.NoiseTexture,
                                  input_kwargs={'W': 0.8, 'Scale': 10.0},
                                  attrs={'noise_dimensions': '4D'})

    multiply_8 = nw.new_node(Nodes.Math,
                             input_kwargs={0: noise_texture_1.outputs["Fac"], 1: group_input_2.outputs["Ynoise"]},
                             attrs={'operation': 'MULTIPLY'})

    add_2 = nw.new_node(Nodes.Math,
                        input_kwargs={0: multiply_7, 1: multiply_8})

    combine_xyz_2 = nw.new_node(Nodes.CombineXYZ,
                                input_kwargs={'X': add, 'Y': add_2})

    group_input_1 = nw.new_node(Nodes.GroupInput,
                                expose_input=[('NodeSocketGeometry', 'Mesh', None),
                                              ('NodeSocketVector', 'Vector', (0.0, 0.0, 0.0)),
                                              ('NodeSocketFloat', 'Scale', 40.0),
                                              ('NodeSocketFloat', 'Xscale', 1.0),
                                              ('NodeSocketFloat', 'Yscale', 1.0),
                                              ('NodeSocketFloat', 'Xnoise', 0.02),
                                              ('NodeSocketFloat', 'Ynoise', 0.02),
                                              ('NodeSocketFloat', 'Offset', 0.0002)])

    multiply_8 = nw.new_node(Nodes.VectorMath, input_kwargs={0: combine_xyz_2, 1: group_input_1.outputs["Scale"]},
                             attrs={'operation': 'MULTIPLY'})

    separate_xyz = nw.new_node(Nodes.SeparateXYZ, input_kwargs={'Vector': multiply_8})

    nodegrid = nw.new_node(nodegroup_node_grid().name, input_kwargs={'Value': separate_xyz.outputs["Y"]})

    greater_than = nw.new_node(Nodes.Compare,
                               input_kwargs={0: nodegrid.outputs["floor1"], 1: separate_xyz.outputs["Y"]},
                               attrs={'operation': 'LESS_THAN'})

    less_than = nw.new_node(Nodes.Compare, input_kwargs={0: nodegrid.outputs["floor1"], 1: separate_xyz.outputs["Y"]})

    nodegrid_1 = nw.new_node(nodegroup_node_grid().name, input_kwargs={'Value': separate_xyz.outputs["X"]})

    combine_xyz = nw.new_node(Nodes.CombineXYZ,
                              input_kwargs={'X': nodegrid_1.outputs["floor2"], 'Y': nodegrid.outputs["floor1"]})

    multiply_9 = nw.new_node(Nodes.VectorMath, input_kwargs={0: less_than, 1: combine_xyz},
                             attrs={'operation': 'MULTIPLY'})

    combine_xyz_1 = nw.new_node(Nodes.CombineXYZ,
                                input_kwargs={'X': nodegrid_1.outputs["floor1"], 'Y': nodegrid.outputs["floor2"]})

    multiply_10 = nw.new_node(Nodes.VectorMath, input_kwargs={0: greater_than, 1: combine_xyz_1},
                              attrs={'operation': 'MULTIPLY'})

    add_3 = nw.new_node(Nodes.VectorMath,
                        input_kwargs={0: multiply_9.outputs["Vector"], 1: multiply_10.outputs["Vector"]})

    subtract_1 = nw.new_node(Nodes.VectorMath, input_kwargs={0: multiply_8, 1: add_3}, attrs={'operation': 'SUBTRACT'})

    distance = nw.new_node(Nodes.VectorMath, input_kwargs={0: multiply_8, 1: add_3}, attrs={'operation': 'DISTANCE'})

    add_4 = nw.new_node(Nodes.Math, input_kwargs={0: distance.outputs["Value"], 1: 0.0100})

    less_than_1 = nw.new_node(Nodes.Compare, input_kwargs={0: add_4, 1: 0.5000}, attrs={'operation': 'LESS_THAN'})

    greater_than_1 = nw.new_node(Nodes.Compare, input_kwargs={0: add_4, 1: 0.5000})

    multiply_11 = nw.new_node(Nodes.VectorMath, input_kwargs={0: less_than, 1: combine_xyz_1},
                              attrs={'operation': 'MULTIPLY'})

    multiply_12 = nw.new_node(Nodes.VectorMath, input_kwargs={0: greater_than, 1: combine_xyz},
                              attrs={'operation': 'MULTIPLY'})

    add_5 = nw.new_node(Nodes.VectorMath,
                        input_kwargs={0: multiply_11.outputs["Vector"], 1: multiply_12.outputs["Vector"]})

    subtract_2 = nw.new_node(Nodes.VectorMath, input_kwargs={0: multiply_8, 1: add_5}, attrs={'operation': 'SUBTRACT'})

    multiply_13 = nw.new_node(Nodes.VectorMath,
                              input_kwargs={0: greater_than_1, 1: subtract_2.outputs["Vector"]},
                              attrs={'operation': 'MULTIPLY'})

    _multiply_add = nw.new_node(Nodes.VectorMath,
                                input_kwargs={0: subtract_1.outputs["Vector"], 1: less_than_1,
                                              2: multiply_13.outputs["Vector"]},
                                attrs={'operation': 'MULTIPLY_ADD'})

    multiply_add = nw.new_node(Nodes.VectorMath,
                               input_kwargs={0: _multiply_add, 1: (1, -1, 1)},
                               attrs={'operation': 'MULTIPLY'})

    multiply_14 = nw.new_node(Nodes.VectorMath, input_kwargs={0: greater_than_1, 1: add_5},
                              attrs={'operation': 'MULTIPLY'})

    multiply_add_1 = nw.new_node(Nodes.VectorMath,
                                 input_kwargs={0: add_3, 1: less_than_1, 2: multiply_14.outputs["Vector"]},
                                 attrs={'operation': 'MULTIPLY_ADD'})

    noise_texture = nw.new_node(Nodes.NoiseTexture,
                                input_kwargs={'Vector': multiply_add_1, 'W': sample_range(-10, 10), 'Scale': 33.0000},
                                attrs={'noise_dimensions': '4D'})

    subtract_3 = nw.new_node(Nodes.MapRange,
                             input_kwargs={0: noise_texture.outputs["Fac"], 1: 0.26, 2: 0.74, 3: -0.5, 4: 0.5},
                             attrs={'clamp': True}
                             )

    sine_1 = nw.new_node(Nodes.Math, input_kwargs={0: subtract_3}, attrs={'operation': 'SINE'})

    cosine_1 = nw.new_node(Nodes.Math, input_kwargs={0: subtract_3}, attrs={'operation': 'COSINE'})

    combine_xyz_color = nw.new_node(Nodes.CombineXYZ, input_kwargs={'X': sine_1, 'Y': cosine_1, 'Z': 0.0000})

    add_6 = nw.new_node(Nodes.VectorMath, input_kwargs={0: combine_xyz_color.outputs["Vector"], 1: multiply_add},
                        attrs={'operation': 'DOT_PRODUCT'})

    distance_1 = nw.new_node(Nodes.VectorMath, input_kwargs={0: multiply_8, 1: add_5}, attrs={'operation': 'DISTANCE'})

    add_7 = nw.new_node(Nodes.Math, input_kwargs={0: distance_1.outputs["Value"], 1: 0.0100})

    multiply_17 = nw.new_node(Nodes.Math, input_kwargs={0: greater_than_1, 1: add_7}, attrs={'operation': 'MULTIPLY'})

    multiply_add_2 = nw.new_node(Nodes.Math, input_kwargs={0: add_4, 1: less_than_1, 2: multiply_17},
                                 attrs={'operation': 'MULTIPLY_ADD'})

    multiply_18 = nw.new_node(Nodes.Math, input_kwargs={0: multiply_add_2, 1: 2.0000}, attrs={'operation': 'MULTIPLY'})

    multiply_19 = nw.new_node(Nodes.MapRange,
                              input_kwargs={0: multiply_18, 1: 0.9156, 2: 1.0000, 3: 0.0000, 4: 0.5},
                              attrs={'clamp': True}
                              )

    subtract_4 = nw.new_node(Nodes.Math, input_kwargs={0: add_6, 1: multiply_19}, attrs={'operation': 'SUBTRACT'})

    subtract_5 = nw.new_node(Nodes.Math, input_kwargs={0: subtract_4, 1: 0.0000}, attrs={'operation': 'SUBTRACT'})

    normal = nw.new_node(Nodes.InputNormal)

    multiply_20 = nw.new_node(Nodes.VectorMath, input_kwargs={0: subtract_5, 1: normal},
                              attrs={'operation': 'MULTIPLY'})

    multiply_21 = nw.new_node(Nodes.VectorMath,
                              input_kwargs={0: multiply_20.outputs["Vector"], 1: group_input.outputs["Offset"]},
                              attrs={'operation': 'MULTIPLY'})

    set_position = nw.new_node(Nodes.SetPosition,
                               input_kwargs={'Geometry': group_input.outputs["Mesh"],
                                             'Offset': multiply_21.outputs["Vector"]})

    capture_attribute_1 = nw.new_node(Nodes.CaptureAttribute,
                                      input_kwargs={'Geometry': set_position, 1: multiply_add_1},
                                      attrs={'data_type': 'FLOAT_VECTOR'})

    capture_attribute_4 = nw.new_node(Nodes.CaptureAttribute,
                                      input_kwargs={'Geometry': capture_attribute_1.outputs["Geometry"],
                                                    1: multiply_19},
                                      attrs={'data_type': 'FLOAT_VECTOR'})

    separate_xyz_7 = nw.new_node(Nodes.SeparateXYZ,
                                 input_kwargs={'Vector': capture_attribute_1.outputs["Attribute"]})

    attribute_statistic = nw.new_node(Nodes.AttributeStatistic,
                                      input_kwargs={'Geometry': capture_attribute_1.outputs["Geometry"],
                                                    2: separate_xyz_7.outputs["X"]})

    subtract_8 = nw.new_node(Nodes.Math,
                             input_kwargs={0: separate_xyz_7.outputs["X"], 1: attribute_statistic.outputs["Min"]},
                             attrs={'operation': 'SUBTRACT'})

    divide = nw.new_node(Nodes.Math,
                         input_kwargs={0: subtract_8, 1: attribute_statistic.outputs["Range"]},
                         attrs={'operation': 'DIVIDE'})

    attribute_statistic_1 = nw.new_node(Nodes.AttributeStatistic,
                                        input_kwargs={'Geometry': capture_attribute_1.outputs["Geometry"],
                                                      2: separate_xyz_7.outputs["Y"]})

    subtract_9 = nw.new_node(Nodes.Math,
                             input_kwargs={0: separate_xyz_7.outputs["Y"], 1: attribute_statistic_1.outputs["Min"]},
                             attrs={'operation': 'SUBTRACT'})

    divide_1 = nw.new_node(Nodes.Math,
                           input_kwargs={0: subtract_9, 1: attribute_statistic_1.outputs["Range"]},
                           attrs={'operation': 'DIVIDE'})

    combine_xyz_3 = nw.new_node(Nodes.CombineXYZ,
                                input_kwargs={'X': divide, 'Y': divide_1})

    group_output = nw.new_node(Nodes.GroupOutput,
                               input_kwargs={'Geometry': capture_attribute_4.outputs["Geometry"],
                                             'attr2': combine_xyz_3,
                                             'attr5': capture_attribute_4.outputs["Attribute"]})


def shader_fish_body_handfish_spotted(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    texture_coordinate = nw.new_node(Nodes.TextureCoord)

    voronoi_texture = nw.new_node(Nodes.VoronoiTexture,
                                  input_kwargs={'Vector': texture_coordinate.outputs["Generated"], 'Scale': 40.0000,
                                                'Randomness': 1.0000, 'Smoothness': 0.8},
                                  attrs={'feature': 'SMOOTH_F1'})

    base_hue = U(0.05, 0.055)
    bright_color = hsv2rgba(
        base_hue, U(0.3, .6), U(0.5, 0.8))
    dark_color = hsv2rgba(
        base_hue, U(0.8, .9), U(0.0, 0.1))
    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': voronoi_texture.outputs["Distance"]})
    color_ramp.color_ramp.interpolation = "EASE"
    color_ramp.color_ramp.elements.new(0)
    color_ramp.color_ramp.elements[0].position = 0.0000
    color_ramp.color_ramp.elements[0].color = dark_color
    color_ramp.color_ramp.elements[1].position = U(0.05, 0.2)
    color_ramp.color_ramp.elements[1].color = [0.1286, 0.0444, 0.0109, 1.0000]
    color_ramp.color_ramp.elements[2].position = 1.0000
    color_ramp.color_ramp.elements[2].color = bright_color

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
                                  input_kwargs={'Base Color': color_ramp.outputs["Color"], 'Metallic': 0.4000,
                                                'Specular': 0.2000})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf},
                                  attrs={'is_active_output': True})


def shader_fish_body_handfish(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    value_shift = log_uniform(2, 10)

    base_hue = uniform(0, 0.02)

    bright_color = hsv2rgba(
        base_hue, uniform(0.6, .8), log_uniform(0.2, 0.4)
    )
    dark_color = hsv2rgba(
        (base_hue + uniform(-0.02, 0.02)) % 1,
        uniform(0.6, .8),
        log_uniform(0.1, 0.2)
    )
    light_color = hsv2rgba(base_hue, uniform(0.0, 0.1), log_uniform(0.2, 1.0))
    specular = uniform(0.6, 0.8)
    specular_tint = *([uniform(0, 1)] * 3), 1
    clearcoat = uniform(0.2, 0.8)
    roughness = uniform(0.4, 0.6)
    metallic = uniform(0.4, 0.5)
    x, y, z = nw.separate(nw.new_node(Nodes.NewGeometry).outputs["Position"])
    color = build_color_ramp(
        nw,
        nw.new_node(
            Nodes.MapRange,
            [
                nw.new_node(
                    Nodes.MusgraveTexture,
                    [nw.combine(x, nw.math("ABSOLUTE", y), z)],
                    input_kwargs={"Scale": log_uniform(5, 8)},
                ),
                -1,
                1,
                0,
                1,
            ],
        ),
        [0.0, 0.3, 0.7, 1.0],
        [bright_color, bright_color, dark_color, dark_color],
    )
    ratio = nw.new_node(Nodes.Attribute, attrs={"attribute_name": "ratio"}).outputs[
        "Fac"
    ]
    # color = nw.new_node(Nodes.MixRGB, [ratio, light_color, color])
    bsdf = nw.new_node(
        Nodes.PrincipledBSDF,
        input_kwargs={
            "Base Color": color,
            "Metallic": metallic,
            "Roughness": roughness,
            "Specular IOR Level": specular,
            "Specular_Tint": specular_tint, #check this is ok
            "Coat Weight": clearcoat,
        },
    )
    return bsdf


def geometry_fish_body(nw: NodeWrangler, rand=True, **input_kwargs):
    # Code generated using version 2.4.3 of the node_transpiler
    group_input = nw.new_node(Nodes.GroupInput)

    UV = nw.new_node(nodegroup_UV().name,
                     input_kwargs={'Vector': nw.expose_input('UVMap', attribute='UVMap', dtype='NodeSocketVector')})

    scales = nw.new_node(nodegroup_scales().name,
                         input_kwargs={'Mesh': group_input, 'Vector': UV, 'Scale': 6, 'Xscale': 0.3, 'Yscale': 12.0,
                                       'Offset': 0.002})
    if rand:
        scales.inputs['Scale'].default_value = sample_ratio(6, 2 / 3, 3 / 2)
        scales.inputs['Xscale'].default_value = sample_range(0.2, 0.3)
        scales.inputs['Yscale'].default_value = sample_range(8, 12)
        scales.inputs['Xnoise'].default_value = sample_range(0.1, 0.3)
        scales.inputs['Ynoise'].default_value = sample_range(0.1, 0.3)

    noise_texture = nw.new_node(Nodes.NoiseTexture,
                                input_kwargs={'Scale': 50.0},
                                attrs={'noise_dimensions': '4D'})
    if rand:
        noise_texture.inputs['W'].default_value = sample_range(-2, 2)

    add = nw.new_node(Nodes.Math,
                      input_kwargs={0: noise_texture.outputs["Fac"], 1: -0.5})

    normal = nw.new_node(Nodes.InputNormal)

    multiply = nw.new_node(Nodes.VectorMath,
                           input_kwargs={0: add, 1: normal},
                           attrs={'operation': 'MULTIPLY'})

    value = nw.new_node(Nodes.Value)
    value.outputs[0].default_value = 0.002

    multiply_1 = nw.new_node(Nodes.VectorMath,
                             input_kwargs={0: multiply.outputs["Vector"], 1: value},
                             attrs={'operation': 'MULTIPLY'})

    set_position = nw.new_node(Nodes.SetPosition,
                               input_kwargs={'Geometry': scales.outputs["Geometry"],
                                             'Offset': multiply_1.outputs["Vector"]})

    group_output = nw.new_node(Nodes.GroupOutput,
                               input_kwargs={'Geometry': set_position,
                                             'attr2': scales.outputs['attr2'],
                                             'attr5': scales.outputs['attr5']})


@node_utils.to_nodegroup('nodegroup_gradient_color', singleton=False, type='ShaderNodeTree')
def nodegroup_gradient_color(nw: NodeWrangler, **input_args):
    # Code generated using version 2.4.3 of the node_transpiler

    attribute_5 = nw.new_node(Nodes.Attribute,
                              attrs={'attribute_name': 'Color variations'})

    separate_xyz = nw.new_node(Nodes.SeparateXYZ,
                               input_kwargs={'Vector': attribute_5.outputs["Vector"]})

    group_input = nw.new_node(Nodes.GroupInput,
                              expose_input=[('NodeSocketFloat', 'Value', 0.5),
                                            # ('NodeSocketColor', 'Color1', (1.0, 1.0, 1.0, 1.0)),
                                            # ('NodeSocketColor', 'Color2', (0.5268, 0.6724, 0.5186, 1.0)),
                                            # ('NodeSocketColor', 'Color3', (0.8055, 0.6284, 0.2728, 1.0)),
                                            # ('NodeSocketColor', 'Color4', (0.838, 0.5269, 0.0338, 1.0)),
                                            # ('NodeSocketColor', 'Color5', (0.0397, 0.0175, 0.0028, 1.0)),
                                            ('NodeSocketFloat', 'Value1', -0.2)])

    multiply = nw.new_node(Nodes.Math,
                           input_kwargs={0: separate_xyz.outputs["Y"], 1: group_input.outputs["Value"]},
                           attrs={'operation': 'MULTIPLY'})

    subtract = nw.new_node(Nodes.Math,
                           input_kwargs={0: separate_xyz.outputs["X"], 1: multiply},
                           attrs={'operation': 'SUBTRACT'})

    map_range = nw.new_node(Nodes.MapRange,
                            input_kwargs={'Value': subtract, 1: group_input.outputs["Value1"]})

    colorramp_1 = nw.new_node(Nodes.ColorRamp,
                              input_kwargs={'Fac': map_range.outputs["Result"]})
    colorramp_1.color_ramp.elements.new(0)
    colorramp_1.color_ramp.elements.new(0)
    colorramp_1.color_ramp.elements.new(0)
    colorramp_1.color_ramp.elements[0].position = 0.0945
    colorramp_1.color_ramp.elements[0].color = input_args["Color1"]
    colorramp_1.color_ramp.elements[1].position = 0.2045
    colorramp_1.color_ramp.elements[1].color = input_args["Color2"]
    colorramp_1.color_ramp.elements[2].position = 0.3159
    colorramp_1.color_ramp.elements[2].color = input_args["Color3"]
    colorramp_1.color_ramp.elements[3].position = 0.4977
    colorramp_1.color_ramp.elements[3].color = input_args["Color4"]
    colorramp_1.color_ramp.elements[4].position = 0.7568
    colorramp_1.color_ramp.elements[4].color = input_args["Color5"]

    group_output = nw.new_node(Nodes.GroupOutput,
                               input_kwargs={'Color': colorramp_1.outputs["Color"]})


@node_utils.to_nodegroup('nodegroup_noise_color', singleton=False, type='ShaderNodeTree')
def nodegroup_noise_color(nw: NodeWrangler):
    # Code generated using version 2.4.3 of the node_transpiler

    texture_coordinate_3 = nw.new_node(Nodes.TextureCoord)

    mapping_3 = nw.new_node(Nodes.Mapping,
                            input_kwargs={'Vector': texture_coordinate_3.outputs["Generated"]})

    group_input = nw.new_node(Nodes.GroupInput,
                              expose_input=[('NodeSocketFloat', 'Scale', 10.0),
                                            ('NodeSocketColor', 'Color1', (0.7379, 0.2623, 0.0648, 1.0)),
                                            ('NodeSocketColor', 'Color2', (0.5029, 0.4287, 0.1079, 1.0))])

    noise_texture_8 = nw.new_node(Nodes.NoiseTexture,
                                  input_kwargs={'Vector': mapping_3, 'W': U(-5, 5),
                                                'Scale': group_input.outputs["Scale"]},
                                  attrs={'noise_dimensions': '4D'})

    colorramp_9 = nw.new_node(Nodes.ColorRamp,
                              input_kwargs={'Fac': noise_texture_8.outputs["Fac"]})
    colorramp_9.color_ramp.elements[0].position = U(0, 0.5)
    colorramp_9.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    colorramp_9.color_ramp.elements[1].position = 1.0
    colorramp_9.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)

    mix_12 = nw.new_node(Nodes.MixRGB,
                         input_kwargs={'Fac': colorramp_9.outputs["Color"], 'Color1': group_input.outputs["Color1"],
                                       'Color2': group_input.outputs["Color2"]})

    group_output = nw.new_node(Nodes.GroupOutput,
                               input_kwargs={"Color": mix_12})


def apply(obj, geo_kwargs=None, shader_kwargs={}, **kwargs):
    attributes = [
        'Color variations',
        'offset2'
    ]

    if random.random() < 0.5:
        shader = shader_fish_body_handfish
    else:
        shader = shader_fish_body_handfish_spotted
    surface.add_geomod(obj, geometry_fish_body, input_kwargs=geo_kwargs, attributes=attributes, apply=True)
    surface.add_material(obj, shader, input_kwargs=shader_kwargs)


if __name__ == "__main__":
    for i in range(1):
        bpy.ops.wm.open_mainfile(filepath='../creatures/dev_fish5.blend')
        i = 0
        for obj in bpy.data.objects:
            if obj.name.find('Nurb') >= 0:
                infinigen.assets.materials.fishfin.apply_handfish(obj)
                i += 1
        fn = os.path.join(os.path.abspath(os.curdir), 'dev_scene_test_fish_nurb2.blend')
        bpy.ops.wm.save_as_mainfile(filepath=fn)
