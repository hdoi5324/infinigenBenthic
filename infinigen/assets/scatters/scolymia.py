# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Lingjie Mei


import numpy as np
from numpy.random import uniform as U

from infinigen.assets.underwater.scolymia import ScolymiaFactory
from infinigen.core.nodes.node_wrangler import NodeWrangler
from infinigen.core.placement.factory import AssetFactory, make_asset_collection
from infinigen.core.placement.instance_scatter import scatter_instances


def apply(obj, n=8, selection=None):
    n_species = np.random.randint(2, 5)
    factories = list(ScolymiaFactory(np.random.randint(1e5)) for i in range(n_species))
    scolymia = make_asset_collection(factories, name='scolymia',
                                              weights=np.random.uniform(0.5, 1, len(factories)), n=n,
                                              verbose=True)


    scale = 0.1 # U(0.1, 0.2) # scale of scolymia

    def ground_offset(nw: NodeWrangler):
        return nw.uniform(-.2 * scale, 0.2 * scale)

    scatter_obj = scatter_instances(
        base_obj=obj, collection=scolymia,
        vol_density=U(0.5, 5), # density across surface
        ground_offset=ground_offset,
        scale=scale, scale_rand=U(-0.1, 0.1),
        selection=selection,
        min_spacing=1.0)

    return scatter_obj, scolymia
