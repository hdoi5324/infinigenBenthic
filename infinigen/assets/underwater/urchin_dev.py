from infinigen.core.nodes.node_wrangler import NodeWrangler, Nodes, isnode, infer_output_socket, geometry_node_group_empty_new

from infinigen.core.nodes.node_info import Nodes
import infinigen.core.util.blender as butil
from infinigen.assets.utils.decorate import assign_material, geo_extension, separate_loose
from infinigen.assets.utils.object import new_icosphere
from infinigen.core import surface


obj = new_icosphere(subdivisions=4)
surface.add_geomod(obj, geo_extension, apply=True)
butil.apply_transform(obj)
width_pct=25
butil.modify_mesh(obj, 'BEVEL', offset_type='PERCENT', width_pct=width_pct, angle_limit=0)
mod = obj.modifiers.new(name="mine", type='NODES')
group = geometry_node_group_empty_new()
mod.node_group = group
mod.show_viewport = True
attributes=['spike', 'girdle']
domains=['FACE'] * 2
input_attributes = [None] * 128
input_args = []
objs = [obj]
nw = NodeWrangler(mod)
geometry = nw.new_node(Nodes.GroupInput, expose_input=[('NodeSocketGeometry', 'Geometry', None)])
face_vertices = nw.new_node(Nodes.FaceNeighbors)
selection = nw.boolean_math('AND', nw.compare('GREATER_EQUAL', face_vertices, 5),
                                    nw.bernoulli(0.98))
girdle_height = 0.1
# Extrude initial girdle using faces with more than 5 sides.
geometry, top, _ = nw.new_node(Nodes.ExtrudeMesh, [geometry, selection, None, girdle_height]).outputs
# Extrude another little bit.
geometry, top, girdle = nw.new_node(Nodes.ExtrudeMesh, [geometry, top, None, 1e-3]).outputs
# Shrink this little bit by a scale
geometry = nw.new_node(Nodes.ScaleElements, [geometry, top, .6]) 
# Extrude the smaller face back towards base
geometry, top, _ = nw.new_node(Nodes.ExtrudeMesh, [geometry, top, None, -girdle_height]).outputs
perturb = 0.1
extrude_height = 1.0
# Create a slightly offset to normal face for extrusion of spikes.
direction = nw.scale(nw.add(nw.new_node(Nodes.InputNormal), nw.uniform([-perturb] * 3, [perturb] * 3)),
                     nw.uniform(.5 * extrude_height, extrude_height))
# Extrude spikes
geometry, top, side = nw.new_node(Nodes.ExtrudeMesh, [geometry, top, direction]).outputs
# Reduce top of spike
geometry = nw.new_node(Nodes.ScaleElements, [geometry, top, .2])
spike = nw.boolean_math('OR', top, side)
nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': geometry, 'Spike': spike, 'Girdle': girdle})
butil.apply_modifiers(obj, "mine")

levels = 1
butil.modify_mesh(obj, 'SUBSURF', apply=True, levels=levels, render_levels=levels)

obj.scale = [2 / max(obj.dimensions)] * 3
obj.scale[-1] *= log_uniform(.6, 1.2)
butil.apply_transform(obj)
adapt_mesh_resolution(obj, face_size, method='subdiv_by_area')
obj = separate_loose(obj)
butil.modify_mesh(obj, 'DISPLACE', texture=bpy.data.textures.new(name='urchin', type='STUCCI'),
                  strength=.005, mid_level=0)
surface.add_geomod(obj, self.geo_material_index, apply=True, input_attributes=[None, 'spike', 'girdle'])
assign_material(obj, self.materials)
self.animate_stretch(obj)
tag_object(obj, 'urchin')