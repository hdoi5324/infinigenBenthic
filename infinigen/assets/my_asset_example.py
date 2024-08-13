import sys
import bpy
from mathutils import Vector
import gin

from infinigen.assets.corals.generate import *
from infinigen.assets.creatures.fish import FishFactory
from infinigen.assets.creatures.jellyfish import JellyfishFactory
from infinigen.assets.objects.creatures.crustacean import *
from infinigen.assets.objects.underwater import ScolymiaFactory
from infinigen.assets.objects.underwater import UrchinFactory
from infinigen.assets.objects.underwater import SeaweedFactory
#importlib.reload(UrchinFactory)

def get_class(class_name):
    return eval(class_name)

seed = 1
i = 0
j = 0
gap = 5
asset_classes = ["Fish", "Crab", "Lobster", "SpinyLobster", "Jellyfish",
    "LeatherCoral", "StarCoral", "TableCoral", "CauliflowerCoral", "BrainCoral", 
    "HoneycombCoral", "BushCoral", "TwigCoral", "TubeCoral", "FanCoral", "ElkhornCoral", "Scolymia", "Urchin"]
for asset in asset_classes:
    obj = get_class(asset + "Factory")(seed).spawn_asset(100)
    obj.location = (i*gap, j*gap, 0)
    i += 1
    if ((i+1)) % 5 == 0:
        j += 1

for k in range(k):
    obj = get_class("SeaweedFactory")(k).spawn_asset(100)
    obj.location = (i*gap, j*gap, 0)
    i += 1
    if ((i+1)) % 5 == 0:
        j += 1