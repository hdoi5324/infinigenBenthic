# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Mingzhe Wang


import os, sys
import numpy as np
import math as ma
from infinigen.assets.materials.utils.surface_utils import clip, sample_range, sample_ratio, sample_color, geo_voronoi_noise
import bpy
import mathutils
from numpy.random import uniform, normal, randint
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.nodes import node_utils
from infinigen.core.util.color import color_category
from infinigen.core import surface
import random

def shader_fin_handfish(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    attribute = nw.new_node(Nodes.Attribute, attrs={'attribute_name': 'Bump'})

    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': attribute.outputs["Color"]})
    color_ramp.color_ramp.elements[0].position = 0.0227
    color_ramp.color_ramp.elements[0].color = [0.0000, 0.0000, 0.0000, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.1432
    color_ramp.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]

    noise_texture = nw.new_node(Nodes.NoiseTexture, input_kwargs={'W': -0.7867, 'Scale': 20.0000},
                                attrs={'noise_dimensions': '4D'})

    color_ramp_1 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture.outputs["Fac"]})
    color_ramp_1.color_ramp.elements.new(0)
    color_ramp_1.color_ramp.elements[0].position = 0.0000
    color_ramp_1.color_ramp.elements[0].color = [0.1215, 0.1095, 0.0708, 1.0000]
    color_ramp_1.color_ramp.elements[1].position = 0.6727
    color_ramp_1.color_ramp.elements[1].color = [0.5711, 0.269, 0.211, 1.0000]
    color_ramp_1.color_ramp.elements[2].position = 1.0000
    color_ramp_1.color_ramp.elements[2].color = [0.0465, 0.1026, 0.0651, 1.0000]

    noise_texture_1 = nw.new_node(Nodes.NoiseTexture, input_kwargs={'W': 1.9311, 'Scale': 10.0000},
                                  attrs={'noise_dimensions': '4D'})

    color_ramp_2 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture_1.outputs["Fac"]})
    color_ramp_2.color_ramp.elements[0].position = 0.0045
    color_ramp_2.color_ramp.elements[0].color = [0.3231, 0.0953, 0.0630, 1.0000]
    color_ramp_2.color_ramp.elements[1].position = 0.5364
    color_ramp_2.color_ramp.elements[1].color = [0.7, 0.26, 0.21, 1.0000]

    mix = nw.new_node(Nodes.Mix,
                      input_kwargs={0: color_ramp.outputs["Color"], 6: color_ramp_1.outputs["Color"],
                                    7: color_ramp_2.outputs["Color"]},
                      attrs={'data_type': 'RGBA'})

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={'Base Color': mix.outputs[2]})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf},
                                  attrs={'is_active_output': True})


def apply(obj, geo_kwargs={}, shader_kwargs={}, **kwargs):
    shader = shader_fin_handfish
    surface.add_material(obj, shader, input_kwargs=shader_kwargs)