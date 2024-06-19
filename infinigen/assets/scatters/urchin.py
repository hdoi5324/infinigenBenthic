# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Lingjie Mei


import numpy as np
from numpy.random import uniform as U

from infinigen.assets.underwater.urchin import UrchinFactory
from infinigen.core.nodes.node_wrangler import NodeWrangler
from infinigen.core.placement.factory import AssetFactory, make_asset_collection
from infinigen.core.placement.instance_scatter import scatter_instances


def apply(obj, n=5, selection=None, density=U(0.5, 3)):
    n_species = np.random.randint(8, 15)
    factories = list(UrchinFactory(np.random.randint(1e5+668), extrude_height=("clip_gaussian", U(1.5, 2.5), 0.7, 0.5, 5.0)) for _ in range(n_species))
    urchin = make_asset_collection(factories, name='blackspinyurchin',
                                              weights=np.random.uniform(0.5, 1, len(factories)), n=n,
                                              verbose=True)

    scale = U(0.07, 0.11) # scale of urchins

    def ground_offset(nw: NodeWrangler):
        return nw.uniform(.5 * scale, .8 * scale)

    scatter_obj = scatter_instances(
        base_obj=obj, collection=urchin,
        density=density, # density across surface
        ground_offset=ground_offset,
        scale=scale, scale_rand=U(-0.2, 0.2),
        scale_rand_axi=U(-0.1, 0.1),
        selection=selection,
        min_spacing=0.15)

    return scatter_obj, urchin
