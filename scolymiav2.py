import bpy
import mathutils
from numpy.random import uniform, normal, randint
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.nodes import node_utils
from infinigen.core.util.color import color_category
from infinigen.core import surface



def shader_scolymia_001(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': (0.0083, 0.0549, 0.0007, 1.0000), 'Subsurface': 0.1193, 'Subsurface Color': (0.0083, 0.0549, 0.0007, 1.0000), 'Roughness': 0.5089, 'Transmission': 0.1292})
    
    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

@node_utils.to_nodegroup('nodegroup_node_group', singleton=False, type='GeometryNodeTree')
def nodegroup_node_group(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    group_input = nw.new_node(Nodes.GroupInput,
        expose_input=[('NodeSocketFloatDistance', 'Radius', 1.0000),
            ('NodeSocketFloat', 'Segments', 0.0000)])
    
    multiply = nw.new_node(Nodes.Math, input_kwargs={0: group_input.outputs["Radius"], 1: -0.2000}, attrs={'operation': 'MULTIPLY'})
    
    combine_xyz = nw.new_node(Nodes.CombineXYZ, input_kwargs={'Z': multiply})
    
    transform_geometry = nw.new_node(Nodes.Transform, input_kwargs={'Translation': combine_xyz})
    
    curve_circle = nw.new_node(Nodes.CurveCircle,
        input_kwargs={'Resolution': group_input.outputs["Segments"], 'Radius': group_input.outputs["Radius"]})
    
    multiply_1 = nw.new_node(Nodes.Math, input_kwargs={0: group_input.outputs["Radius"], 1: 0.4000}, attrs={'operation': 'MULTIPLY'})
    
    curve_circle_1 = nw.new_node(Nodes.CurveCircle, input_kwargs={'Resolution': group_input.outputs["Segments"], 'Radius': multiply_1})
    
    curve_to_mesh = nw.new_node(Nodes.CurveToMesh,
        input_kwargs={'Curve': curve_circle.outputs["Curve"], 'Profile Curve': curve_circle_1.outputs["Curve"]})
    
    join_geometry = nw.new_node(Nodes.JoinGeometry, input_kwargs={'Geometry': [transform_geometry, curve_to_mesh]})
    
    multiply_2 = nw.new_node(Nodes.Math, input_kwargs={0: group_input.outputs["Radius"], 1: 0.8000}, attrs={'operation': 'MULTIPLY'})
    
    multiply_3 = nw.new_node(Nodes.Math, input_kwargs={0: group_input.outputs["Radius"], 1: 0.4000}, attrs={'operation': 'MULTIPLY'})
    
    cylinder = nw.new_node('GeometryNodeMeshCylinder',
        input_kwargs={'Vertices': group_input.outputs["Segments"], 'Fill Segments': 12, 'Radius': multiply_2, 'Depth': multiply_3})
    
    union = nw.new_node(Nodes.MeshBoolean,
        input_kwargs={'Mesh 2': [join_geometry, cylinder.outputs["Mesh"]]},
        attrs={'operation': 'UNION'})
    
    group_output = nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': union.outputs["Mesh"]}, attrs={'is_active_output': True})

def shader_scolymia(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': (0.0138, 0.0546, 0.0093, 1.0000), 'Subsurface': 0.1000, 'Subsurface Color': (0.0265, 0.0546, 0.0220, 1.0000), 'Roughness': 0.5907, 'Transmission': 0.1441})
    
    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def geometry_nodes(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    torus_shape = nw.new_node(nodegroup_node_group().name, input_kwargs={'Segments': 48.0000}, label='TorusShape')
    
    subdivide_mesh = nw.new_node(Nodes.SubdivideMesh, input_kwargs={'Mesh': torus_shape})
    
    subdivision_surface_1 = nw.new_node(Nodes.SubdivisionSurface, input_kwargs={'Mesh': subdivide_mesh})
    
    position_1 = nw.new_node(Nodes.InputPosition)
    
    separate_xyz_1 = nw.new_node(Nodes.SeparateXYZ, input_kwargs={'Vector': position_1})
    
    arctan2 = nw.new_node(Nodes.Math,
        input_kwargs={0: separate_xyz_1.outputs["Y"], 1: separate_xyz_1.outputs["X"]},
        attrs={'operation': 'ARCTAN2'})
    
    degrees = nw.new_node(Nodes.Math, input_kwargs={0: arctan2, 1: 0.1900}, attrs={'operation': 'DEGREES'})
    
    divide = nw.new_node(Nodes.Math, input_kwargs={0: degrees, 1: 45.0000}, attrs={'operation': 'DIVIDE'})
    
    fract = nw.new_node(Nodes.Math, input_kwargs={0: divide}, attrs={'operation': 'FRACT'})
    
    absolute = nw.new_node(Nodes.Math, input_kwargs={0: fract}, attrs={'operation': 'ABSOLUTE'})
    
    less_than = nw.new_node(Nodes.Compare, input_kwargs={0: absolute, 1: 0.1500}, attrs={'operation': 'LESS_THAN'})
    
    normal = nw.new_node(Nodes.InputNormal)
    
    scale = nw.new_node(Nodes.VectorMath, input_kwargs={0: normal, 'Scale': 0.5000}, attrs={'operation': 'SCALE'})
    
    extrude_mesh_1 = nw.new_node(Nodes.ExtrudeMesh,
        input_kwargs={'Mesh': subdivision_surface_1, 'Selection': less_than, 'Offset': scale.outputs["Vector"], 'Offset Scale': 0.0800, 'Individual': False})
    
    normal_1 = nw.new_node(Nodes.InputNormal)
    
    voronoi_texture = nw.new_node(Nodes.VoronoiTexture,
        input_kwargs={'Scale': 9.0000, 'Smoothness': 0.2000, 'Randomness': 0.4000},
        attrs={'feature': 'F2', 'voronoi_dimensions': '2D'})
    
    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': voronoi_texture.outputs["Distance"]})
    color_ramp.color_ramp.interpolation = "B_SPLINE"
    color_ramp.color_ramp.elements[0].position = 0.6473
    color_ramp.color_ramp.elements[0].color = [0.0000, 0.0000, 0.0000, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.8727
    color_ramp.color_ramp.elements[1].color = [0.5000, 0.5000, 0.5000, 1.0000]
    
    scale_1 = nw.new_node(Nodes.VectorMath,
        input_kwargs={0: color_ramp.outputs["Color"], 'Scale': 0.9000},
        attrs={'operation': 'SCALE'})
    
    scale_2 = nw.new_node(Nodes.VectorMath,
        input_kwargs={0: normal_1, 'Scale': scale_1.outputs["Vector"]},
        attrs={'operation': 'SCALE'})
    
    multiply = nw.new_node(Nodes.Math, input_kwargs={0: 0.1000, 1: 0.6000}, attrs={'operation': 'MULTIPLY'})
    
    scale_3 = nw.new_node(Nodes.VectorMath,
        input_kwargs={0: scale_2.outputs["Vector"], 'Scale': multiply},
        attrs={'operation': 'SCALE'})
    
    set_position_1 = nw.new_node(Nodes.SetPosition,
        input_kwargs={'Geometry': extrude_mesh_1.outputs["Mesh"], 'Offset': scale_3.outputs["Vector"]})
    
    wave_texture = nw.new_node(Nodes.WaveTexture,
        input_kwargs={'Scale': 1.8000, 'Distortion': 5.0000, 'Detail': 5.0000, 'Detail Scale': 0.5000, 'Detail Roughness': 1.0000},
        attrs={'wave_type': 'RINGS', 'rings_direction': 'SPHERICAL'})
    
    extrude_mesh = nw.new_node(Nodes.ExtrudeMesh,
        input_kwargs={'Mesh': set_position_1, 'Offset': wave_texture.outputs["Color"], 'Offset Scale': 0.0100, 'Individual': False})
    
    set_shade_smooth_1 = nw.new_node(Nodes.SetShadeSmooth, input_kwargs={'Geometry': extrude_mesh.outputs["Mesh"]})
    
    noise_texture = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Scale': 0.3000, 'Detail': 0.0000, 'Roughness': 0.0000, 'Distortion': 0.1000})
    
    set_position = nw.new_node(Nodes.SetPosition,
        input_kwargs={'Geometry': set_shade_smooth_1, 'Offset': noise_texture.outputs["Fac"]})
    
    set_material = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': set_position, 'Material': surface.shaderfunc_to_material(shader_scolymia_001)})
    
    group_output = nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': set_material}, attrs={'is_active_output': True})



def apply(obj, selection=None, **kwargs):
    surface.add_geomod(obj, geometry_nodes, selection=selection, attributes=[])
    surface.add_material(obj, shader_scolymia, selection=selection)