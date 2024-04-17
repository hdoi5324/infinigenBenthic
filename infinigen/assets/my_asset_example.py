import bpy
import importlib

from infinigen.assets.underwater.urchin import UrchinFactory
importlib.reload(UrchinFactory)

seed = 0
obj = UrchinFactory(seed).spawn_asset(0)
