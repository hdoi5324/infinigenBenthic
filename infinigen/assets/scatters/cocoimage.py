# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.


import numpy as np
from numpy.random import uniform, normal as N

from infinigen.assets.objects.underwater import ImagePlaneFactory
from infinigen.core.placement.factory import make_asset_collection
from infinigen.core.placement.instance_scatter import scatter_instances


def apply(obj, selection=None, density=5e3, data_path="../BenthicSynData/outputs",
          dataset_campaign="squidle_handfish_pretrain"):
    fac = ImagePlaneFactory(np.random.randint(1e5), data_path=data_path, dataset_campaign=dataset_campaign)
    col = make_asset_collection(fac, name='cocoimage', n=15)
    scatter_obj = scatter_instances(
        base_obj=obj, collection=col,
        density=density, min_spacing=.08,
        scale=.1, scale_rand=N(0.5, 0.2),
        selection=selection
    )
    return scatter_obj
