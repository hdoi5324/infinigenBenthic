# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.


from numpy.random import uniform as U, normal as N

from infinigen.assets.objects.underwater.cocoimageplane import CocoImageplaneFactory
from infinigen.core.placement.factory import make_asset_collection
from infinigen.core.placement.instance_scatter import scatter_instances


def apply(obj, tmp_image_dir="/tmp", scene_seed=3e5, selection=None, density=20, data_path="../BenthicSynData/outputs",
          dataset_campaign="sq_hand_train85_n200v2", category_id=1):
    fac = CocoImageplaneFactory(scene_seed, tmp_image_dir=tmp_image_dir, data_path=data_path,
                                dataset_campaign=dataset_campaign, category_id=category_id)
    col = make_asset_collection(fac, name=fac.name, n=4)
    scatter_obj = scatter_instances(
        base_obj=obj, collection=col,
        density=density, min_spacing=.08,
        scale=.1, scale_rand=N(0.5, 0.2),
        ground_offset=U(0.05, .1),
        selection=selection
    )
    return scatter_obj
