from infinigen.assets.creatures.util.creature_parser import parse_part
import bpy
from pathlib import Path

import numpy as np
debug = True
if debug:
    import pydevd_pycharm
    pydevd_pycharm.settrace('localhost', port=52000, stdoutToServer=True, stderrToServer=True)

# Export nurb data from nurb object in blender
from pathlib import Path
from infinigen.assets.creatures.util.creature_parser import parse_part
NURBS_BASE_PATH = Path(__file__).parent/'nurbs_data'
nurbs_part = bpy.context.active_object
handles = parse_part(nurbs_part, None, "./infinigen/assets/creatures/parts/nurbs_data")

#Load nurb data and create blender object
from infinigen.assets.creatures.util.geometry.nurbs import blender_nurbs
from infinigen.assets.creatures.parts.generic_nurbs import load_nurbs
nurb_data = 'body_fish_pufferfish'
nurb = load_nurbs(nurb_data)
blender_nurbs(nurb)


