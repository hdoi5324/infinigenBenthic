from infinigen.assets.corals.generate import *


#importlib.reload(ScolymiaFactory)

def get_class(class_name):
    return eval(class_name)

seed = 1
i = 0
j = 0
k=3
gap = 5
asset_classes = ["Lichen"]
for asset in asset_classes:
    for k in range(k):
        obj = get_class(asset + "Factory")(k).spawn_asset(1)
        #obj = get_class(asset + "Factory")(k, min_spike_scale=0.8, extrude_height=(1.0, 1.5), spike_hue=0.365, z_scale=(0.5, 0.8)).spawn_asset(1)
        obj.location = (i*gap, j*gap, 0)
        i += 1
        if ((i+1)) % 5 == 0:
            i=0
            j += 1
