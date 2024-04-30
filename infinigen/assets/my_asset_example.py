import bpy
import sys
import importlib
import bpy
import mathutils
from mathutils import Vector
import gin
import numpy as np
from numpy.random import uniform, normal, randint


from infinigen.assets.corals.generate import *
from infinigen.assets.creatures.fish import FishFactory
from infinigen.assets.creatures.jellyfish import JellyfishFactory
from infinigen.assets.creatures.crustacean import *
from infinigen.assets.underwater.scolymia import ScolymiaFactory
from infinigen.assets.underwater.urchin import UrchinFactory
#importlib.reload(UrchinFactory)

def get_class(class_name):
    return eval(class_name)

seed = 1
i = 0
j = 0
asset_classes = ["Fish", "Crab", "Lobster", "SpinyLobster", "Jellyfish",
    "LeatherCoral", "StarCoral", "TableCoral", "CauliflowerCoral", "BrainCoral", 
    "HoneycombCoral", "BushCoral", "TwigCoral", "TubeCoral", "FanCoral", "ElkhornCoral", "Scolymia", "Urchin"]
for asset in asset_classes:
    obj = get_class(asset + "Factory")(seed).spawn_asset(100)
    obj.location = (i, j, 0)
    i += 3
    if (j+1) % 5 == 0:
        j += 1
