import bpy
import mathutils
from numpy.random import uniform, normal, randint
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.assets.utils.object import new_icosphere
from infinigen.core.nodes import node_utils
from infinigen.core.util.color import color_category
from infinigen.core import surface


import bpy
import numpy as np

from infinigen.core.placement.factory import AssetFactory
from infinigen.core.util.math import FixedSeed

class ScolymiaFactory(AssetFactory):

    def __init__(self, factory_seed):
        super().__init__(factory_seed)
        with FixedSeed(factory_seed):
            self.my_randomizable_parameter = np.random.uniform(0, 100)

    def create_asset(self, **kwargs) -> bpy.types.Object:
        obj = new_icosphere(subdivisions=4)
        surface.add_geomod(obj, geometry_nodes, selection=None, attributes=[])
        # todo: add scaling
        # todo: add material
        # todo: add distortion
        return obj

def geometry_nodes(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    curve_circle_1 = nw.new_node(Nodes.CurveCircle, input_kwargs={'Resolution': 64, 'Radius': 1.7000})

    curve_circle = nw.new_node(Nodes.CurveCircle, input_kwargs={'Resolution': 64, 'Radius': 0.8000})

    curve_to_mesh = nw.new_node(Nodes.CurveToMesh,
        input_kwargs={'Curve': curve_circle_1.outputs["Curve"], 'Profile Curve': curve_circle.outputs["Curve"]})

    cylinder = nw.new_node('GeometryNodeMeshCylinder', input_kwargs={'Fill Segments': 24, 'Radius': 1.2000, 'Depth': 0.2000})

    join_geometry = nw.new_node(Nodes.JoinGeometry, input_kwargs={'Geometry': [curve_to_mesh, cylinder.outputs["Mesh"]]})

    wave_texture_2 = nw.new_node(Nodes.WaveTexture,
        input_kwargs={'Scale': 6.0000, 'Distortion': 8.0000, 'Detail': 1.5000, 'Phase Offset': -1.0000},
        attrs={'rings_direction': 'Z', 'wave_type': 'RINGS', 'bands_direction': 'Z'})

    wave_texture_1 = nw.new_node(Nodes.WaveTexture,
        input_kwargs={'Scale': 6.0000, 'Distortion': 9.5000, 'Phase Offset': 2.5000},
        attrs={'wave_profile': 'SAW', 'wave_type': 'RINGS', 'bands_direction': 'Z'})

    mix = nw.new_node(Nodes.Mix, input_kwargs={2: wave_texture_2.outputs["Color"], 3: wave_texture_1.outputs["Color"]})

    map_range = nw.new_node(Nodes.MapRange,
        input_kwargs={'Value': mix.outputs["Result"], 1: 0.7000, 2: 5.0000},
        attrs={'clamp': False})

    extrude_mesh = nw.new_node(Nodes.ExtrudeMesh,
        input_kwargs={'Mesh': join_geometry, 'Offset Scale': map_range.outputs["Result"], 'Individual': False})

    subdivision_surface = nw.new_node(Nodes.SubdivisionSurface,
        input_kwargs={'Mesh': extrude_mesh.outputs["Mesh"], 'Level': 2, 'Edge Crease': 0.4000, 'Vertex Crease': 0.4000})

    group_output = nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': subdivision_surface}, attrs={'is_active_output': True})



def apply(obj, selection=None, **kwargs):
    surface.add_geomod(obj, geometry_nodes, selection=selection, attributes=[])
