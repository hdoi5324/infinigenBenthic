# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Alexander Raistrick


from numpy.random import uniform as U, randint

from infinigen.assets.underwater.plasticbag import make_plasticbag_collection
from infinigen.core.placement.instance_scatter import scatter_instances


def apply(obj, selection=None, density=0.5, **kwargs):
    col = make_plasticbag_collection(randint(100), 5)
    return scatter_instances(
        base_obj=obj,
        collection=col,
        scale=.8, scale_rand=U(0, 0.5),
        scale_rand_axi=U(0, 0.9),
        density=density,
        ground_offset=U(0.1, 1.5),
        selection=selection,
        taper_density=True)
