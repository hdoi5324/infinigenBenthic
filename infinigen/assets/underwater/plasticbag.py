import logging

import bpy
import numpy as np
from numpy.random import randint

from infinigen.assets.creatures.util import cloth_sim
from infinigen.assets.utils.object import new_cube
from infinigen.assets.utils.tag import tag_object
from infinigen.core import surface
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.placement.factory import AssetFactory, make_asset_collection
from infinigen.core.util.math import FixedSeed

logger = logging.getLogger(__name__)


class PlasticbagFactory(AssetFactory):

    def __init__(self, factory_seed):
        super().__init__(factory_seed)
        with FixedSeed(factory_seed):
            self.my_randomizable_parameter = np.random.uniform(0, 100)

    def create_asset(self, **kwargs) -> bpy.types.Object:
        obj = new_cube()

        settings = dict(
            compression_stiffness=1200,
            tension_stiffness=1200,
            shear_stiffness=1200,
            bending_stiffness=3000,

            tension_damping=100,
            compression_damping=100,
            shear_damping=100,
            bending_damping=100,

            air_damping=5,
            mass=0.1,
            uniform_pressure_force=2
        )

        cloth_sim.bake_cloth(obj, settings, {}, 1, randint(10))
        obj.name = "plasticbag"
        surface.add_geomod(obj, geometry_nodes, selection=None, attributes=[])
        surface.add_material(obj, shader_polyethylene, selection=None)
        tag_object(obj, 'plasticbag')
        return obj


def shader_polyethylene(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    translucent_bsdf = nw.new_node(Nodes.TranslucentBSDF, input_kwargs={'Color': (0.4275, 0.4174, 0.8000, 1.0000)})

    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': translucent_bsdf},
                                  attrs={'is_active_output': True})


def geometry_nodes(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    group_input = nw.new_node(Nodes.GroupInput, expose_input=[('NodeSocketGeometry', 'Geometry', None)])

    transform_geometry = nw.new_node(Nodes.Transform,
                                     input_kwargs={'Geometry': group_input.outputs["Geometry"],
                                                   'Translation': (0.0000, 0.0000, 0.5000),
                                                   'Scale': (0.3500, 0.0010, 0.5000)})

    subdivide_mesh = nw.new_node(Nodes.SubdivideMesh, input_kwargs={'Mesh': transform_geometry, 'Level': 5})

    position = nw.new_node(Nodes.InputPosition)

    separate_xyz = nw.new_node(Nodes.SeparateXYZ, input_kwargs={'Vector': position})

    absolute = nw.new_node(Nodes.Math, input_kwargs={0: separate_xyz.outputs["X"]}, attrs={'operation': 'ABSOLUTE'})

    greater_than = nw.new_node(Nodes.Math, input_kwargs={0: absolute, 1: 0.3000}, attrs={'operation': 'GREATER_THAN'})

    absolute_1 = nw.new_node(Nodes.Math, input_kwargs={0: separate_xyz.outputs["X"]}, attrs={'operation': 'ABSOLUTE'})

    less_than = nw.new_node(Nodes.Math, input_kwargs={0: absolute_1, 1: 0.2000}, attrs={'operation': 'LESS_THAN'})

    op_or = nw.new_node(Nodes.BooleanMath, input_kwargs={0: greater_than, 1: less_than}, attrs={'operation': 'OR'})

    greater_than_1 = nw.new_node(Nodes.Math, input_kwargs={0: separate_xyz.outputs["Z"], 1: 0.8000},
                                 attrs={'operation': 'GREATER_THAN'})

    op_and = nw.new_node(Nodes.BooleanMath, input_kwargs={0: op_or, 1: greater_than_1})

    delete_geometry = nw.new_node(Nodes.DeleteGeometry, input_kwargs={'Geometry': subdivide_mesh, 'Selection': op_and})

    transform_geometry_1 = nw.new_node(Nodes.Transform, input_kwargs={'Geometry': delete_geometry})

    noise_texture = nw.new_node(Nodes.NoiseTexture,
                                input_kwargs={'Vector': position, 'Scale': 1.7000, 'Detail': 1.2000,
                                              'Roughness': 0.2000, 'Distortion': 0.1000})

    subtract = nw.new_node(Nodes.Math, input_kwargs={0: noise_texture.outputs["Fac"]}, attrs={'operation': 'SUBTRACT'})

    combine_xyz = nw.new_node(Nodes.CombineXYZ, input_kwargs={'X': subtract, 'Y': subtract})

    set_position = nw.new_node(Nodes.SetPosition,
                               input_kwargs={'Geometry': transform_geometry_1, 'Offset': combine_xyz})

    set_shade_smooth = nw.new_node(Nodes.SetShadeSmooth, input_kwargs={'Geometry': set_position, 'Shade Smooth': False})

    group_output = nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': set_shade_smooth},
                               attrs={'is_active_output': True})


def apply(obj, selection=None, **kwargs):
    surface.add_geomod(obj, geometry_nodes, selection=selection, attributes=[])
    surface.add_material(obj, shader_polyethylene, selection=selection)


def make_plasticbag_collection(seed, n=5):
    logger.debug(f'Starting make_plastic bags({seed=})')

    weights = []
    child_factories = []
    for i in range(n):
        fac, _ = PlasticbagFactory(seed + i)
        child_factories.append(fac)
        weights.append(1.0)

    weights = np.array(weights)
    weights /= np.sum(weights)  # normalize to 1

    col = make_asset_collection(child_factories, n, verbose=True, weights=weights)

    return col
