# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Mingzhe Wang

from numpy.random import uniform as U

from infinigen.core import surface
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.util.color import hsv2rgba


def shader_fin_handfish(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    attribute = nw.new_node(Nodes.Attribute, attrs={'attribute_name': 'Bump'})

    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': attribute.outputs["Color"]})
    color_ramp.color_ramp.elements[0].position = 0.0227
    color_ramp.color_ramp.elements[0].color = [0.0000, 0.0000, 0.0000, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.1432
    color_ramp.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]

    noise_texture_1 = nw.new_node(Nodes.NoiseTexture, input_kwargs={'W': 1.9311, 'Scale': 10.0000},
                                  attrs={'noise_dimensions': '4D'})

    color_ramp_2 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture_1.outputs["Fac"]})
    color_ramp_2.color_ramp.elements[0].position = 0.0045
    color_ramp_2.color_ramp.elements[0].color = [0.3231, 0.0953, 0.0630, 1.0000]
    color_ramp_2.color_ramp.elements[1].position = 0.5364
    color_ramp_2.color_ramp.elements[1].color = [0.7000, 0.2600, 0.2100, 1.0000]

    mix = nw.new_node(Nodes.Mix,
                      input_kwargs={0: color_ramp.outputs["Color"], 6: color_ramp_2.outputs["Color"],
                                    7: (0.5000, 0.3281, 0.2408, 1.0000)},
                      attrs={'data_type': 'RGBA'})

    principled_bsdf = nw.new_node(
        Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': mix.outputs[2]},
        attrs={"subsurface_method": "BURLEY"})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf},
                                  attrs={'is_active_output': True})


def shader_fin_handfish_spotted(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    attribute = nw.new_node(Nodes.Attribute, attrs={'attribute_name': 'Bump'})

    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': attribute.outputs["Color"]})
    color_ramp.color_ramp.interpolation = "EASE"
    color_ramp.color_ramp.elements[0].position = 0.0373
    color_ramp.color_ramp.elements[0].color = [0.0000, 0.0000, 0.0000, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.0982
    color_ramp.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]

    texture_coordinate = nw.new_node(Nodes.TextureCoord)

    voronoi_texture = nw.new_node(Nodes.VoronoiTexture,
                                  input_kwargs={'Vector': texture_coordinate.outputs["Generated"], 'Scale': 40.0000,
                                                'Smoothness': 0.8000},
                                  attrs={'feature': 'SMOOTH_F1'})

    color_ramp_3 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': voronoi_texture.outputs["Distance"]})
    color_ramp_3.color_ramp.interpolation = "B_SPLINE"
    color_ramp_3.color_ramp.elements.new(0)
    color_ramp_3.color_ramp.elements[0].position = 0.0000
    color_ramp_3.color_ramp.elements[0].color = [0.0369, 0.0130, 0.0048, 1.0000]
    color_ramp_3.color_ramp.elements[1].position = 0.4341
    color_ramp_3.color_ramp.elements[1].color = [0.1286, 0.0444, 0.0109, 1.0000]
    color_ramp_3.color_ramp.elements[2].position = 1.0000
    color_ramp_3.color_ramp.elements[2].color = [1.0000, 0.7662, 0.6669, 1.0000]

    base_hue = U(0.05, 0.055)
    bright_color = hsv2rgba(
        base_hue, U(0.3, .6), U(0.5, 0.8))
    mix = nw.new_node(Nodes.Mix,
                      input_kwargs={0: color_ramp.outputs["Color"], 6: color_ramp_3.outputs["Color"],
                                    7: bright_color},
                      attrs={'blend_type': 'LIGHTEN', 'clamp_factor': False, 'data_type': 'RGBA'})

    principled_bsdf = nw.new_node(
        Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': mix.outputs[2]},
        attrs={"subsurface_method": "BURLEY"})

    material_output = nw.new_node(
        Nodes.MaterialOutput,
        input_kwargs={'Surface': principled_bsdf},
        attrs={'is_active_output': True})


def apply(obj, geo_kwargs={}, shader_kwargs={}, **kwargs):
    if geo_kwargs.get("spotted", False):
        shader = shader_fin_handfish_spotted
    else:
        shader = shader_fin_handfish
    surface.add_material(obj, shader, input_kwargs=shader_kwargs)
