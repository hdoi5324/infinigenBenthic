# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Zeyu Ma
# Acknowledgement: This file draws inspiration from https://www.youtube.com/watch?v=y02x-p_0wP0 by Sam Bowman


import gin
from mathutils import Vector

from infinigen.core.nodes.node_wrangler import Nodes
from infinigen.core import surface
from infinigen.core.util.organization import SurfaceTypes
from infinigen.core.util.math import FixedSeed
from infinigen.core.util.random import random_general as rg

type = SurfaceTypes.SDFPerturb
mod_name = "geo_SAND"
name = "sand"

@gin.configurable('shader')
def shader_SAND(
        nw,
        color=("palette", "desert"),
        random_seed=0,
        wet=False,
        wet_part=("uniform", 0.2, 0.25),
        *args,
        **kwargs
    ):
    nw.force_input_consistency()

    with FixedSeed(random_seed):
        position = (nw.new_node("ShaderNodeTexCoord", []), 3)
        assert(color is not None)
        if wet:
            position = nw.new_node('ShaderNodeNewGeometry')
            factor = nw.scalar_divide(nw.separate(position)[2], 3) # this needs to be consistent with value in coast.gin
            factor = nw.scalar_add(factor, -0.5, nw.new_node(Nodes.NoiseTexture, input_kwargs={"Scale": 0.1}))
            sand_color = nw.new_node(Nodes.ColorRamp, [factor])
            sand_color.color_ramp.elements[0].position = rg(wet_part)
            sand_color.color_ramp.elements[0].color = rg(("color_category", "wet_sand"))
            sand_color.color_ramp.elements[1].position = sand_color.color_ramp.elements[0].position + 0.11
            sand_color.color_ramp.elements[1].color = rg(("color_category", "dry_sand"))
            roughness = nw.new_node(Nodes.ColorRamp, [factor])
            roughness.color_ramp.elements[0].position = sand_color.color_ramp.elements[0].position / 2
            roughness.color_ramp.elements[0].color = (0.1, 0.1, 0.1, 0.1)
            roughness.color_ramp.elements[1].position = sand_color.color_ramp.elements[1].position
            roughness.color_ramp.elements[1].color = (1, 1, 1, 1)
        else:
            sand_color = tuple(rg(color))
            roughness = 1.0
        bsdf_sand = nw.new_node("ShaderNodeBsdfPrincipled", input_kwargs={
            "Base Color": sand_color,
            "Roughness": roughness,
        })
    return bsdf_sand

@gin.configurable('geo')
def geo_SAND(nw,
    n_waves=3,
    wave_scale=("log_uniform", 0.2, 4),
    wave_distortion=4,
    noise_scale=125,
    noise_detail=9, # tune down if there are numerical spikes
    noise_roughness=0.9,
    selection=None,
):
    nw.force_input_consistency()
    normal = nw.new_node("GeometryNodeInputNormal", [])
    position = nw.new_node("GeometryNodeInputPosition", [])

    offsets = []
    for i in range(n_waves):
        wave_scale_node = nw.new_value(rg(wave_scale), f"wave_scale_{i}")
        
        
        position_shift0 = nw.new_node(Nodes.Vector, label=f"position_shift_0_{i}")
        position_shift0.vector = nw.get_position_translation_seed(f"position_shift_0_{i}")
        position_shift1 = nw.new_node(Nodes.Vector, label=f"position_shift_1_{i}")
        position_shift1.vector = nw.get_position_translation_seed(f"position_shift_1_{i}")
        position_shift2 = nw.new_node(Nodes.Vector, label=f"position_shift_2_{i}")
        position_shift2.vector = nw.get_position_translation_seed(f"position_shift_2_{i}")
        position_shift3 = nw.new_node(Nodes.Vector, label=f"position_shift_3_{i}")
        position_shift3.vector = nw.get_position_translation_seed(f"position_shift_3_{i}")

        mag = nw.power(1e5, nw.scalar_sub(nw.new_node(Nodes.NoiseTexture, input_kwargs={
            "Vector": nw.add(position, position_shift3),
            "Scale": 0.1,
        }), 0.6))
        mag.use_clamp = 1
        offsets.append(nw.multiply(
            nw.add(
                nw.new_node(Nodes.WaveTexture, [
                    nw.add(
                        position,
                        position_shift0,
                        (nw.new_node(Nodes.NoiseTexture, input_kwargs={
                            "Scale": nw.new_value(1, "warp_scale"),
                            "Detail": nw.new_value(9, "warp_detail"),
                        }), 1),
                    ),
                    wave_scale_node,
                    wave_distortion
                ]),
                nw.new_node(Nodes.WaveTexture, [
                    nw.add(position, position_shift1),
                    nw.scalar_multiply(wave_scale_node, 0.98),
                    wave_distortion
                ]),
                nw.multiply(
                    nw.new_node(Nodes.NoiseTexture, [
                        nw.add(position, position_shift2),
                        None,
                        noise_scale,
                        noise_detail,
                        noise_roughness
                    ]),
                    Vector([1] * 3),
                )
            ),
            normal,
            mag,
            Vector([0.01] * 3)
        ))
    offset = nw.add(*offsets)
    groupinput = nw.new_node(Nodes.GroupInput)
    if selection is not None:
        offset = nw.multiply(offset, surface.eval_argument(nw, selection))
    set_position = nw.new_node(Nodes.SetPosition, input_kwargs={"Geometry": groupinput,  "Offset": offset})
    groupoutput = nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': set_position})


def shader_rocky_ground(
        nw,
        color=("palette", "desert"),
        random_seed=0,
        wet=False,
        wet_part=("uniform", 0.2, 0.25),
        *args,
        **kwargs
    ):
    # Code generated using version 2.6.5 of the node_transpiler

    texture_coordinate = nw.new_node(Nodes.TextureCoord)

    noise_texture_4 = nw.new_node(Nodes.NoiseTexture,
                                  input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': 4.0000})

    color_ramp_5 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture_4.outputs["Fac"]})
    color_ramp_5.color_ramp.interpolation = "EASE"
    color_ramp_5.color_ramp.elements[0].position = 0.3527
    color_ramp_5.color_ramp.elements[0].color = [0.0000, 0.0000, 0.0000, 1.0000]
    color_ramp_5.color_ramp.elements[1].position = 0.5018
    color_ramp_5.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]

    noise_texture_2 = nw.new_node(Nodes.NoiseTexture,
                                  input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': 14.0000,
                                                'Roughness': 0.8000})

    color_ramp_4 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture_2.outputs["Fac"]})
    color_ramp_4.color_ramp.elements.new(0)
    color_ramp_4.color_ramp.elements.new(0)
    color_ramp_4.color_ramp.elements[0].position = 0.0000
    color_ramp_4.color_ramp.elements[0].color = [0.0000, 0.0000, 0.0000, 1.0000]
    color_ramp_4.color_ramp.elements[1].position = 0.2364
    color_ramp_4.color_ramp.elements[1].color = [0.0014, 0.0642, 0.0115, 1.0000]
    color_ramp_4.color_ramp.elements[2].position = 0.5273
    color_ramp_4.color_ramp.elements[2].color = [0.0090, 0.0550, 0.0163, 1.0000]
    color_ramp_4.color_ramp.elements[3].position = 0.7527
    color_ramp_4.color_ramp.elements[3].color = [0.0295, 0.0856, 0.0380, 1.0000]

    noise_texture_1 = nw.new_node(Nodes.NoiseTexture,
                                  input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': 8.0000})

    voronoi_texture = nw.new_node(Nodes.VoronoiTexture,
                                  input_kwargs={'Vector': noise_texture_1.outputs["Color"], 'Scale': 8.0000,
                                                'Randomness': 0.5000},
                                  attrs={'feature': 'SMOOTH_F1'})

    color_ramp_1 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': voronoi_texture.outputs["Distance"]})
    color_ramp_1.color_ramp.interpolation = "EASE"
    color_ramp_1.color_ramp.elements[0].position = 0.2000
    color_ramp_1.color_ramp.elements[0].color = [0.9332, 0.9332, 0.9332, 1.0000]
    color_ramp_1.color_ramp.elements[1].position = 0.2255
    color_ramp_1.color_ramp.elements[1].color = [0.0000, 0.0000, 0.0000, 1.0000]

    voronoi_texture_1 = nw.new_node(Nodes.VoronoiTexture,
                                    input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': 8.0000,
                                                  'Randomness': 0.8000},
                                    attrs={'feature': 'F2'})

    color_ramp_2 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': voronoi_texture_1.outputs["Distance"]})
    color_ramp_2.color_ramp.elements[0].position = 0.1855
    color_ramp_2.color_ramp.elements[0].color = [0.9332, 0.9332, 0.9332, 1.0000]
    color_ramp_2.color_ramp.elements[1].position = 0.4636
    color_ramp_2.color_ramp.elements[1].color = [0.0000, 0.0000, 0.0000, 1.0000]

    mix = nw.new_node(Nodes.Mix,
                      input_kwargs={0: 1.0000, 6: color_ramp_1.outputs["Color"], 7: color_ramp_2.outputs["Color"]},
                      attrs={'blend_type': 'ADD', 'data_type': 'RGBA'})

    noise_texture = nw.new_node(Nodes.NoiseTexture,
                                input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': 30.0000,
                                              'Detail': 2.1000, 'Roughness': 0.8000})

    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture.outputs["Fac"]})
    color_ramp.color_ramp.elements.new(0)
    color_ramp.color_ramp.elements.new(0)
    color_ramp.color_ramp.elements[0].position = 0.1200
    color_ramp.color_ramp.elements[0].color = [1.0000, 0.6133, 0.3730, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.2368
    color_ramp.color_ramp.elements[1].color = [0.0278, 0.0175, 0.0100, 1.0000]
    color_ramp.color_ramp.elements[2].position = 0.4882
    color_ramp.color_ramp.elements[2].color = [1.0000, 0.5659, 0.2409, 1.0000]
    color_ramp.color_ramp.elements[3].position = 0.7055
    color_ramp.color_ramp.elements[3].color = [0.4209, 0.1969, 0.0849, 1.0000]

    mix_1 = nw.new_node(Nodes.Mix,
                        input_kwargs={0: mix.outputs[2], 6: color_ramp.outputs["Color"],
                                      7: (0.0577, 0.0285, 0.0099, 1.0000)},
                        attrs={'data_type': 'RGBA'})

    mix_2 = nw.new_node(Nodes.Mix,
                        input_kwargs={0: color_ramp_5.outputs["Color"], 6: color_ramp_4.outputs["Color"],
                                      7: mix_1.outputs[2]},
                        attrs={'data_type': 'RGBA'})

    color_ramp_3 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': mix_1.outputs[2]})
    color_ramp_3.color_ramp.elements[0].position = 0.0000
    color_ramp_3.color_ramp.elements[0].color = [0.5274, 0.5274, 0.5274, 1.0000]
    color_ramp_3.color_ramp.elements[1].position = 1.0000
    color_ramp_3.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
                                  input_kwargs={'Base Color': mix_2,
                                                'Roughness': color_ramp_3})

    return principled_bsdf

def shader__s_a_n_d_001(
        nw,
        color=("palette", "desert"),
        random_seed=0,
        wet=False,
        wet_part=("uniform", 0.2, 0.25),
        *args,
        **kwargs
    ):
    # Code generated using version 2.6.5 of the node_transpiler

    musgrave_texture = nw.new_node(Nodes.MusgraveTexture, input_kwargs={'Scale': 8.8000})

    subtract = nw.new_node(Nodes.Math, input_kwargs={0: 1.0000, 1: musgrave_texture}, attrs={'operation': 'SUBTRACT'})

    color_ramp_2 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': subtract})
    color_ramp_2.color_ramp.interpolation = "CARDINAL"
    color_ramp_2.color_ramp.elements.new(0)
    color_ramp_2.color_ramp.elements.new(0)
    color_ramp_2.color_ramp.elements[0].position = 0.0000
    color_ramp_2.color_ramp.elements[0].color = [1.0000, 1.0000, 1.0000, 0.1000]
    color_ramp_2.color_ramp.elements[1].position = 0.6000
    color_ramp_2.color_ramp.elements[1].color = [0.9078, 0.9078, 0.9078, 0.3250]
    color_ramp_2.color_ramp.elements[2].position = 0.6547
    color_ramp_2.color_ramp.elements[2].color = [0.0245, 0.0245, 0.0245, 0.5500]
    color_ramp_2.color_ramp.elements[3].position = 1.0000
    color_ramp_2.color_ramp.elements[3].color = [0.0000, 0.0000, 0.0000, 1.0000]

    geometry = nw.new_node(Nodes.NewGeometry)

    separate_xyz = nw.new_node(Nodes.SeparateXYZ, input_kwargs={'Vector': geometry.outputs["Position"]})

    divide = nw.new_node(Nodes.Math, input_kwargs={0: separate_xyz.outputs["Z"], 1: 3.0000},
                         attrs={'operation': 'DIVIDE'})

    geometry_1 = nw.new_node(Nodes.NewGeometry)

    noise_texture = nw.new_node(Nodes.NoiseTexture,
                                input_kwargs={'Vector': geometry_1.outputs["Position"], 'Scale': 0.1000})

    add = nw.new_node(Nodes.Math, input_kwargs={0: -0.5000, 1: noise_texture.outputs["Fac"]})

    add_1 = nw.new_node(Nodes.Math, input_kwargs={0: divide, 1: add})

    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': add_1})
    color_ramp.color_ramp.elements[0].position = 0.2274
    color_ramp.color_ramp.elements[0].color = [0.1045, 0.0700, 0.0334, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.3993
    color_ramp.color_ramp.elements[1].color = [0.1938, 0.1180, 0.0616, 1.0000]

    color_ramp_3 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': color_ramp_2.outputs["Color"]})
    color_ramp_3.color_ramp.elements[0].position = 0.2274
    color_ramp_3.color_ramp.elements[0].color = [0.1045, 0.0259, 0.0130, 1.0000]
    color_ramp_3.color_ramp.elements[1].position = 0.3993
    color_ramp_3.color_ramp.elements[1].color = [0.0186, 0.0125, 0.0077, 1.0000]

    mix = nw.new_node(Nodes.Mix,
                      input_kwargs={0: color_ramp_2.outputs["Color"], 6: color_ramp.outputs["Color"],
                                    7: color_ramp_3.outputs["Color"]},
                      attrs={'data_type': 'RGBA'})

    color_ramp_1 = nw.new_node(Nodes.ColorRamp)
    color_ramp_1.color_ramp.elements[0].position = 0.1137
    color_ramp_1.color_ramp.elements[0].color = [0.1000, 0.1000, 0.1000, 0.1000]
    color_ramp_1.color_ramp.elements[1].position = 0.3374
    color_ramp_1.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
                                  input_kwargs={'Base Color': mix,
                                                'Roughness': color_ramp_1})

    return principled_bsdf

def apply(objs, selection=None, **kwargs):
    surface.add_geomod(objs, geo_SAND, selection=selection)
    surface.add_material(objs, shader_rocky_ground, selection=selection,
        input_kwargs={"obj": objs[0] if isinstance(objs, list) else objs})

if __name__ == "__main__":
    from infinigen.assets.utils.object import new_icosphere
    objs = [new_icosphere(subdivisions=4)]
    apply(objs)