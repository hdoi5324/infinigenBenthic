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
from infinigen.assets.underwater.seaweed import SeaweedFactory
#importlib.reload(ScolymiaFactory)

def get_class(class_name):
    return eval(class_name)

seed = 1
i = 0
j = 0
k=15
gap = 5
asset_classes = ["Scolymia"]
for asset in asset_classes:
    for k in range(k):
        obj = get_class(asset + "Factory")(k).spawn_asset(100)
        obj.location = (i*gap, j*gap, 0)
        i += 1
        if ((i+1)) % 5 == 0:
            i=0
            j += 1