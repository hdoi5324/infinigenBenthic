import bpy
import mathutils
import colorsys

from numpy.random import uniform, normal, randint
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.assets.utils.object import new_icosphere
from infinigen.core.nodes import node_utils
from infinigen.core.util.color import color_category
from infinigen.assets.utils.misc import log_uniform
from infinigen.assets.utils.decorate import assign_material, geo_extension, separate_loose

from infinigen.core import surface
from infinigen.assets.utils.tag import tag_object, tag_nodegroup


import bpy
import numpy as np

from infinigen.core.placement.factory import AssetFactory
from infinigen.core.util.math import FixedSeed

class ScolymiaFactory(AssetFactory):

    def __init__(self, factory_seed):
        super().__init__(factory_seed)
        with FixedSeed(factory_seed):
            self.base_hue = uniform(.3, .34)
            self.materials = [surface.shaderfunc_to_material(shader, self.base_hue) for shader in
                              [self.shader_scolymia]]
            self.my_randomizable_parameter = np.random.uniform(0, 100)

    def create_asset(self, **kwargs) -> bpy.types.Object:
        obj = new_icosphere(subdivisions=4)
        surface.add_geomod(obj, geometry_nodes, selection=None, attributes=[])
        # todo: add scaling
        #surface.add_material(obj, shader_scolymia, selection=None)
        assign_material(obj, self.materials)
        # todo: add distortion
        tag_object(obj, 'scolymia')
        return obj

    def shader_scolymia(self, nw: NodeWrangler, base_hue=0.31):
        return shader_scolymia(nw, base_hue)


@node_utils.to_nodegroup('nodegroup_node_group', singleton=False, type='GeometryNodeTree')
def nodegroup_node_group(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    group_input = nw.new_node(Nodes.GroupInput, expose_input=[('NodeSocketFloatDistance', 'Radius', 1.0000)])

    multiply = nw.new_node(Nodes.Math, input_kwargs={0: group_input.outputs["Radius"], 1: 0.8000},
                           attrs={'operation': 'MULTIPLY'})

    multiply_1 = nw.new_node(Nodes.Math, input_kwargs={0: group_input.outputs["Radius"], 1: 0.4000},
                             attrs={'operation': 'MULTIPLY'})

    cylinder = nw.new_node('GeometryNodeMeshCylinder',
                           input_kwargs={'Fill Segments': 12, 'Radius': multiply, 'Depth': multiply_1})

    multiply_2 = nw.new_node(Nodes.Math, input_kwargs={0: group_input.outputs["Radius"], 1: -0.2000},
                             attrs={'operation': 'MULTIPLY'})

    combine_xyz = nw.new_node(Nodes.CombineXYZ, input_kwargs={'Z': multiply_2})

    transform_geometry = nw.new_node(Nodes.Transform,
                                     input_kwargs={'Geometry': cylinder.outputs["Mesh"], 'Translation': combine_xyz})

    curve_circle_1 = nw.new_node(Nodes.CurveCircle,
                                 input_kwargs={'Resolution': 64, 'Radius': group_input.outputs["Radius"]})

    multiply_3 = nw.new_node(Nodes.Math, input_kwargs={0: group_input.outputs["Radius"], 1: 0.4000},
                             attrs={'operation': 'MULTIPLY'})

    curve_circle = nw.new_node(Nodes.CurveCircle, input_kwargs={'Resolution': 64, 'Radius': multiply_3})

    curve_to_mesh = nw.new_node(Nodes.CurveToMesh,
                                input_kwargs={'Curve': curve_circle_1.outputs["Curve"],
                                              'Profile Curve': curve_circle.outputs["Curve"]})

    join_geometry = nw.new_node(Nodes.JoinGeometry, input_kwargs={'Geometry': [transform_geometry, curve_to_mesh]})

    group_output = nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': join_geometry},
                               attrs={'is_active_output': True})


def shader_scolymia(nw: NodeWrangler, base_hue=0.31):
    # Code generated using version 2.6.5 of the node_transpiler

    transmission = uniform(.0, .2)
    subsurface = uniform(.1, .2)
    roughness = uniform(.5, .8)
    color = *colorsys.hsv_to_rgb(base_hue, uniform(.8, 1.), uniform(.05, .1)), 1
    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={
        'Base Color': color,
        'Roughness': roughness,
        'Subsurface': subsurface,
        'Subsurface Color': color,
        'Transmission': transmission
    })

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf},
                                  attrs={'is_active_output': True})


def geometry_nodes(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    torus_shape = nw.new_node(nodegroup_node_group().name, label='TorusShape')

    set_material = nw.new_node(Nodes.SetMaterial,
                               input_kwargs={'Geometry': torus_shape,
                                             'Material': surface.shaderfunc_to_material(shader_scolymia)})

    position = nw.new_node(Nodes.InputPosition)

    separate_xyz = nw.new_node(Nodes.SeparateXYZ, input_kwargs={'Vector': position})

    greater_than = nw.new_node(Nodes.Math, input_kwargs={0: separate_xyz.outputs["Z"], 1: -0.2500},
                               attrs={'operation': 'GREATER_THAN'})

    wave_texture = nw.new_node(Nodes.WaveTexture,
                               input_kwargs={'Scale': 6.4000, 'Distortion': 3.0000, 'Detail': 5.0000,
                                             'Detail Scale': 0.5000},
                               attrs={'rings_direction': 'SPHERICAL', 'wave_type': 'RINGS'})

    map_range = nw.new_node(Nodes.MapRange, input_kwargs={'Value': wave_texture.outputs["Color"]})

    extrude_mesh = nw.new_node(Nodes.ExtrudeMesh,
                               input_kwargs={'Mesh': set_material, 'Selection': greater_than,
                                             'Offset': map_range.outputs["Result"], 'Offset Scale': 0.1000,
                                             'Individual': False})

    subdivision_surface = nw.new_node(Nodes.SubdivisionSurface, input_kwargs={'Mesh': extrude_mesh.outputs["Mesh"]})

    set_shade_smooth = nw.new_node(Nodes.SetShadeSmooth,
                                   input_kwargs={'Geometry': subdivision_surface, 'Shade Smooth': False})
    distort_scale = normal(0, 0.3)
    noise_texture = nw.new_node(Nodes.NoiseTexture,
                                input_kwargs={'Scale': distort_scale, 'Detail': 0.0000},
                                attrs={'noise_dimensions': '2D'})

    combine_xyz = nw.new_node(Nodes.CombineXYZ, input_kwargs={'Y': noise_texture.outputs["Color"]})

    set_position = nw.new_node(Nodes.SetPosition, input_kwargs={'Geometry': set_shade_smooth, 'Offset': combine_xyz})

    group_output = nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': set_position},
                               attrs={'is_active_output': True})


def apply(obj, selection=None, **kwargs):
    surface.add_geomod(obj, geometry_nodes, selection=selection, attributes=[])
    surface.add_material(obj, shader_scolymia, selection=selection)
