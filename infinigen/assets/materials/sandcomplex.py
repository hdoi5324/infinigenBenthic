# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Zeyu Ma
# Acknowledgement: This file draws inspiration from https://www.youtube.com/watch?v=y02x-p_0wP0 by Sam Bowman


import gin
gin.enter_interactive_mode()
from mathutils import Vector
from numpy.random import uniform

from infinigen.core.nodes.node_wrangler import Nodes
from infinigen.core import surface
from infinigen.core.util.organization import SurfaceTypes
from infinigen.core.util.math import FixedSeed
from infinigen.core.util.random import random_general as rg
from infinigen.core.nodes import node_utils

type = SurfaceTypes.SDFPerturb
mod_name = "geometry_soil"
name = "soil"


@node_utils.to_nodegroup(
    "nodegroup_displacement_to_offset", singleton=False, type="GeometryNodeTree"
)
def nodegroup_displacement_to_offset(nw):
    # Code generated using version 2.3.1 of the node_transpiler

    group_input = nw.new_node(
        Nodes.GroupInput,
        expose_input=[
            ("NodeSocketVector", "Vector", (0.0, 0.0, 0.0)),
            ("NodeSocketFloat", "Magnitude", 1.0),
        ],
    )

    multiply = nw.new_node(
        Nodes.Math,
        input_kwargs={
            0: group_input.outputs["Vector"],
            1: group_input.outputs["Magnitude"],
        },
        attrs={"operation": "MULTIPLY"},
    )

    normal = nw.new_node(Nodes.InputNormal)

    multiply_1 = nw.new_node(
        Nodes.VectorMath,
        input_kwargs={0: multiply, 1: normal},
        attrs={"operation": "MULTIPLY"},
    )

    group_output = nw.new_node(
        Nodes.GroupOutput, input_kwargs={"Vector": multiply_1.outputs["Vector"]}
    )


def nodegroup_pebble(nw):
    if nw.node_group.type == "SHADER":
        position = nw.new_node("ShaderNodeNewGeometry")
    else:
        position = nw.new_node(Nodes.InputPosition)

    # Code generated using version 2.3.1 of the node_transpiler

    noise1_w = nw.new_node(Nodes.Value, label="noise1_w ~ U(0, 10)")
    noise1_w.outputs[0].default_value = uniform(0.0, 10.0)

    group_input = nw.new_node(
        Nodes.GroupInput,
        expose_input=[
            ("NodeSocketFloat", "PebbleScale", 5.0),
            ("NodeSocketFloat", "NoiseMag", 0.2),
        ],
    )

    noise_texture = nw.new_node(
        Nodes.NoiseTexture,
        input_kwargs={"W": noise1_w, "Scale": group_input.outputs["PebbleScale"]},
        attrs={"noise_dimensions": "4D"},
    )

    multiply = nw.new_node(
        Nodes.VectorMath,
        input_kwargs={
            0: noise_texture.outputs["Color"],
            1: group_input.outputs["NoiseMag"],
        },
        attrs={"operation": "MULTIPLY"},
    )

    add = nw.new_node(
        Nodes.VectorMath, input_kwargs={0: multiply.outputs["Vector"], 1: position}
    )

    vornoi1_w = nw.new_node(Nodes.Value, label="vornoi1_w ~ U(0, 10)")
    vornoi1_w.outputs[0].default_value = uniform(0.0, 10.0)

    voronoi_texture_2 = nw.new_node(
        Nodes.VoronoiTexture,
        input_kwargs={
            "Vector": add.outputs["Vector"],
            "W": vornoi1_w,
            "Scale": group_input.outputs["PebbleScale"],
        },
        attrs={"voronoi_dimensions": "4D"},
    )

    group_output = nw.new_node(
        Nodes.GroupOutput,
        input_kwargs={"Distance": voronoi_texture_2.outputs["Distance"]},
    )


@node_utils.to_nodegroup("nodegroup_pebble", singleton=False)
def nodegroup_pebble_geo(nw):
    nw.force_input_consistency()
    nodegroup_pebble(nw)

@node_utils.to_nodegroup("nodegroup_pebble", singleton=False, type="ShaderNodeTree")
def nodegroup_pebble_shader(nw):
    nw.force_input_consistency()
    nodegroup_pebble(nw)



@gin.configurable
def geometry_soil(nw, selection=None, random_seed=0, geometry=True):
    nw.force_input_consistency()
    if nw.node_group.type == "SHADER":
        position = nw.new_node("ShaderNodeNewGeometry")
        normal = (nw.new_node("ShaderNodeNewGeometry"), 1)
    else:
        position = nw.new_node(Nodes.InputPosition)
        normal = nw.new_node(Nodes.InputNormal)

    with FixedSeed(random_seed):
        # Code generated using version 2.3.1 of the node_transpiler

        peb1_size = nw.new_value(uniform(2.0, 5.0), "peb1_size ~ U(2, 5)")
        peb1_noise_mag = nw.new_value(
            (1 / peb1_size.outputs[0].default_value) * uniform(1.5, 2),
            "peb1_noise_mag ~ U(0.1, 0.5)",
        )

        group = nw.new_node(
            nodegroup_pebble_geo().name
            if nw.node_group.type != "SHADER"
            else nodegroup_pebble_shader().name,
            input_kwargs={"PebbleScale": peb1_size, "NoiseMag": peb1_noise_mag},
        )

        peb1_roundness = uniform(0.5, 1.0)
        peb1_amount = uniform(0.2, 0.5)

        colorramp = nw.new_node(
            Nodes.ColorRamp, input_kwargs={"Fac": group}, label="colorramp_VAR"
        )
        colorramp.color_ramp.elements[0].position = 0.0
        colorramp.color_ramp.elements[0].color = (
            peb1_roundness,
            peb1_roundness,
            peb1_roundness,
            1.0,
        )
        colorramp.color_ramp.elements.new(1)
        colorramp.color_ramp.elements[1].color = (
            peb1_roundness / 2,
            peb1_roundness / 2,
            peb1_roundness / 2,
            1.0,
        )
        colorramp.color_ramp.elements[1].position = peb1_amount / 8
        colorramp.color_ramp.elements[2].position = peb1_amount
        colorramp.color_ramp.elements[2].color = (0.0, 0.0, 0.0, 1.0)

        peb2_size = nw.new_value(uniform(5, 9), "peb2_size ~ U(5, 9)")
        peb2_noise_scale = nw.new_value(
            (1 / peb2_size.outputs[0].default_value) * uniform(1.5, 2),
            "peb2_noise_scale ~ U(0.05, 0.2)",
        )

        group_3 = nw.new_node(
            nodegroup_pebble_geo().name
            if nw.node_group.type != "SHADER"
            else nodegroup_pebble_shader().name,
            input_kwargs={"PebbleScale": peb2_size, "NoiseMag": peb2_noise_scale},
        )

        peb2_roundness = uniform(0.3, 0.8)
        peb2_amount = uniform(0.2, 0.5)
        colorramp_2 = nw.new_node(
            Nodes.ColorRamp, input_kwargs={"Fac": group_3}, label="colorramp_2_VAR"
        )
        colorramp_2.color_ramp.elements[0].position = 0.0
        colorramp_2.color_ramp.elements[0].color = (
            peb2_roundness,
            peb2_roundness,
            peb2_roundness,
            1.0,
        )
        colorramp_2.color_ramp.elements.new(1)
        colorramp_2.color_ramp.elements[1].color = (
            peb2_roundness / 2,
            peb2_roundness / 2,
            peb2_roundness / 2,
            1.0,
        )
        colorramp_2.color_ramp.elements[1].position = peb2_amount / 8
        colorramp_2.color_ramp.elements[2].position = peb2_amount
        colorramp_2.color_ramp.elements[2].color = (0.0, 0.0, 0.0, 1.0)

        add = nw.new_node(
            Nodes.Math,
            input_kwargs={
                0: colorramp.outputs["Color"],
                1: colorramp_2.outputs["Color"],
            },
        )

        big_stone = colorramp

        peb3_size = nw.new_value(uniform(12.0, 18.0), "peb3_size ~ U(12, 18)")
        peb3_noise_scale = nw.new_value(
            uniform(0.05, 0.35), "peb3_noise_scale ~ U(0.05, 0.35)"
        )

        group_2 = nw.new_node(
            nodegroup_pebble_geo().name
            if nw.node_group.type != "SHADER"
            else nodegroup_pebble_shader().name,
            input_kwargs={"PebbleScale": peb3_size, "NoiseMag": peb3_noise_scale},
        )

        colorramp_1 = nw.new_node(Nodes.ColorRamp, input_kwargs={"Fac": group_2})
        colorramp_1.color_ramp.elements[0].position = 0.0
        colorramp_1.color_ramp.elements[0].color = (0.15, 0.15, 0.15, 1.0)
        colorramp_1.color_ramp.elements[1].position = 0.9
        colorramp_1.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)

        add_1 = nw.new_node(
            Nodes.Math, input_kwargs={0: add, 1: colorramp_1.outputs["Color"]}
        )

    if geometry:
        offset = nw.new_node(
            nodegroup_displacement_to_offset().name,
            input_kwargs={"Vector": add_1, "Magnitude": 0.1},
        )
        groupinput = nw.new_node(Nodes.GroupInput)
        if selection is not None:
            offset = nw.multiply(offset, surface.eval_argument(nw, selection))
        set_position = nw.new_node(
            Nodes.SetPosition, input_kwargs={"Geometry": groupinput, "Offset": offset}
        )
        nw.new_node(Nodes.GroupOutput, input_kwargs={"Geometry": set_position})
    else:
        return big_stone

def shader_rocky_ground(nw, random_seed=0
    ):
    # Code generated using version 2.6.5 of the node_transpiler

    texture_coordinate = nw.new_node(Nodes.TextureCoord)
    
    noise_texture_2 = nw.new_node(Nodes.NoiseTexture, input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': 15.0000})
    
    color_ramp_3 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture_2.outputs["Fac"]})
    color_ramp_3.color_ramp.interpolation = "EASE"
    color_ramp_3.color_ramp.elements[0].position = 0.3527
    color_ramp_3.color_ramp.elements[0].color = [0.0000, 0.0000, 0.0000, 1.0000]
    color_ramp_3.color_ramp.elements[1].position = 0.5018
    color_ramp_3.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]
    
    texture_coordinate_1 = nw.new_node(Nodes.TextureCoord)
    
    voronoi_texture_2 = nw.new_node(Nodes.VoronoiTexture,
        input_kwargs={'Vector': texture_coordinate_1.outputs["Object"], 'Scale': 8},
        attrs={'feature': 'F2'})
    
    noise_texture_3 = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Vector': voronoi_texture_2.outputs["Color"], 'Scale': 20, 'Roughness': 0.8000})
    
    color_ramp_4 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture_3.outputs["Fac"]})
    color_ramp_4.color_ramp.elements.new(0)
    color_ramp_4.color_ramp.elements.new(0)
    color_ramp_4.color_ramp.elements[0].position = 0.0000
    color_ramp_4.color_ramp.elements[0].color = [0.0000, 0.0000, 0.0000, 1.0000]
    color_ramp_4.color_ramp.elements[1].position = 0.2437
    color_ramp_4.color_ramp.elements[1].color = [0.4380, 0.0120, 0.2609, 1.0000]
    color_ramp_4.color_ramp.elements[2].position = 0.5273
    color_ramp_4.color_ramp.elements[2].color = [0.0090, 0.0550, 0.0163, 1.0000]
    color_ramp_4.color_ramp.elements[3].position = 0.7527
    color_ramp_4.color_ramp.elements[3].color = [0.0532, 0.0034, 0.0393, 1.0000]
    
    noise_texture_4 = nw.new_node(Nodes.NoiseTexture, input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': 8.0000})
    
    voronoi_texture = nw.new_node(Nodes.VoronoiTexture,
        input_kwargs={'Vector': noise_texture_4.outputs["Color"], 'Scale': 15, 'Randomness': 0.5000},
        attrs={'feature': 'SMOOTH_F1'})
    
    color_ramp_5 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': voronoi_texture.outputs["Distance"]})
    color_ramp_5.color_ramp.interpolation = "EASE"
    color_ramp_5.color_ramp.elements[0].position = 0.2000
    color_ramp_5.color_ramp.elements[0].color = [0.9332, 0.9332, 0.9332, 1.0000]
    color_ramp_5.color_ramp.elements[1].position = 0.2255
    color_ramp_5.color_ramp.elements[1].color = [0.0000, 0.0000, 0.0000, 1.0000]
    
    voronoi_texture_1 = nw.new_node(Nodes.VoronoiTexture,
        input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': 8, 'Randomness': 0.8000},
        attrs={'feature': 'F2'})
    
    color_ramp_6 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': voronoi_texture_1.outputs["Distance"]})
    color_ramp_6.color_ramp.elements[0].position = 0.1855
    color_ramp_6.color_ramp.elements[0].color = [0.9332, 0.9332, 0.9332, 1.0000]
    color_ramp_6.color_ramp.elements[1].position = 0.4636
    color_ramp_6.color_ramp.elements[1].color = [0.0000, 0.0000, 0.0000, 1.0000]
    
    mix = nw.new_node(Nodes.Mix,
        input_kwargs={0: 1.0000, 6: color_ramp_5.outputs["Color"], 7: color_ramp_6.outputs["Color"]},
        attrs={'data_type': 'RGBA', 'blend_type': 'ADD'})
    
    noise_texture_5 = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': 30.0000, 'Detail': 2.1000, 'Roughness': 0.8000})
    
    color_ramp_7 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture_5.outputs["Fac"]})
    color_ramp_7.color_ramp.elements.new(0)
    color_ramp_7.color_ramp.elements.new(0)
    color_ramp_7.color_ramp.elements[0].position = 0.1200
    color_ramp_7.color_ramp.elements[0].color = [1.0000, 0.6133, 0.3730, 1.0000]
    color_ramp_7.color_ramp.elements[1].position = 0.2368
    color_ramp_7.color_ramp.elements[1].color = [0.0278, 0.0175, 0.0100, 1.0000]
    color_ramp_7.color_ramp.elements[2].position = 0.4882
    color_ramp_7.color_ramp.elements[2].color = [1.0000, 0.5659, 0.2409, 1.0000]
    color_ramp_7.color_ramp.elements[3].position = 0.7055
    color_ramp_7.color_ramp.elements[3].color = [0.4209, 0.1969, 0.0849, 1.0000]
    
    mix_1 = nw.new_node(Nodes.Mix,
        input_kwargs={0: mix.outputs[2], 6: color_ramp_7.outputs["Color"], 7: (0.0577, 0.0285, 0.0099, 1.0000)},
        attrs={'data_type': 'RGBA'})
    
    mix_2 = nw.new_node(Nodes.Mix,
        input_kwargs={0: color_ramp_3.outputs["Color"], 6: color_ramp_4.outputs["Color"], 7: mix_1.outputs[2]},
        attrs={'data_type': 'RGBA'})
    
    color_ramp_8 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': mix_1.outputs[2]})
    color_ramp_8.color_ramp.elements[0].position = 0.0000
    color_ramp_8.color_ramp.elements[0].color = [0.5274, 0.5274, 0.5274, 1.0000]
    color_ramp_8.color_ramp.elements[1].position = 1.0000
    color_ramp_8.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]
    
    principled_bsdf_2 = nw.new_node(Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': mix_2.outputs[2], 'Roughness': color_ramp_8.outputs["Color"]})

    return principled_bsdf_2


def apply(objs, selection=None, **kwargs):
    surface.add_geomod(objs, geometry_soil, selection=selection)
    surface.add_material(objs, shader_rocky_ground, selection=selection)

if __name__ == "__main__":
    import bpy
    obj = bpy.context.active_object
    apply(obj)