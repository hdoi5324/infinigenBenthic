# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Alexander Raistrick

'''
1. Copy this script into the blender scripting UI
2. Select a Nurbs Cylinder object you have modified into some shape
3. Run the script
'''


#import pdb

import bpy
import numpy as np
import mathutils

from infinigen.assets.utils.geometry import nurbs #lofting, skin_ops
#from infinigen.assets.objects.creatures.util.creature_parser import parse_nurbs_data
#from infinigen.core.util import blender as butil

def parse_nurbs_data(obj, i=0):
    """
    Given a blender object, read it's handles out as a (n,m,3) vertex array

    TODO: Read out knotvector. Function should yield all data necessary to define that NURBS
    """

    assert obj.type == "SURFACE"

    spline = obj.data.splines[i]
    m, n = spline.point_count_u, spline.point_count_v

    points = np.array([p.co for p in spline.points])
    points = points.reshape(n, m, -1)

    return points

vis = True
    
obj = bpy.context.active_object
#for obj in bpy.context.selected_objects:
handles = parse_nurbs_data(obj)[..., :3]
    
# blender uses V = long axis of a cylinder by default, this is not our convention
#handles = handles.transpose(0, 1, 2)
handles = handles.transpose(1, 0, 2)    
    # blender has U = 0 face right, ours faces down
handles = np.roll(handles, 2, axis=1)
    
    
handles = handles[:, ::-1]
print(f"Shape of handles {handles.shape}")

if vis:
    new_obj = nurbs.nurbs(handles, method='blender', face_size=0.05)
    new_obj.location = obj.location + mathutils.Vector((0, 0.5, 0))

path = f'./infinigen/assets/objects/creatures/parts/nurbs_data/{obj.name}.npy'
np.save(path, handles)
print('Saved', path)