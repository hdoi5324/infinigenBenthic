# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Lingjie Mei


import numpy as np
from numpy.random import uniform as U

from infinigen.assets.underwater.urchin import UrchinFactory
from infinigen.core.nodes.node_wrangler import NodeWrangler
from infinigen.core.placement.factory import AssetFactory, make_asset_collection
from infinigen.core.placement.instance_scatter import scatter_instances


def apply(obj, n=5, selection=None, density=U(0.2, 0.8)):
    n_species = np.random.randint(2, 5)
    factories = list(UrchinFactory(np.random.randint(1e5)) for i in range(n_species))
    # Add baby urchin
    factories.append(UrchinFactory(np.random.randint(1e5), min_spike_scale=0.2, spike_prob=.6, extrude_height=(1.0, 3.0)))
    urchin = make_asset_collection(factories, name='blackspinyurchin',
                                              weights=np.random.uniform(0.5, 1, len(factories)), n=n,
                                              verbose=True)

    scale = 0.09 # U(0.03, 0.3) # scale of urchins

    def ground_offset(nw: NodeWrangler):
        return nw.uniform(.4 * scale, .8 * scale)

    scatter_obj = scatter_instances(
        base_obj=obj, collection=urchin,
        vol_density=density, # density across surface
        ground_offset=ground_offset,
        scale=scale, scale_rand=U(-0.1, 0.1),
        scale_rand_axi=U(-0.05, 0.05),
        selection=selection,
        min_spacing=0.05)

    return scatter_obj, urchin
