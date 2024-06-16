# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors:
# - Alexander Raistrick: FishSchoolFactory, basic version of FishFactory, anim & simulation
# - Mingzhe Wang: Fin placement


from collections import defaultdict

import bpy
import gin
import numpy as np
from numpy.random import uniform as U, normal as N, randint

import infinigen.assets.materials.scale
import infinigen.assets.materials.handfishbody
import infinigen.assets.materials.fishbody
from infinigen.assets.materials import fishfin, eyeball
from infinigen.core import surface
from infinigen.assets.materials.utils.surface_utils import sample_range

from infinigen.core.placement.factory import AssetFactory, make_asset_collection

from infinigen.assets.creatures.util import genome
from infinigen.assets.creatures.util.genome import Joint
from infinigen.assets.creatures import parts
from infinigen.assets.creatures.util import creature, joining
from infinigen.assets.creatures.util import cloth_sim
from infinigen.assets.creatures.util.boid_swarm import BoidSwarmFactory

from infinigen.core.util import blender as butil
from infinigen.core.util.math import clip_gaussian, FixedSeed
from infinigen.assets.creatures.util.animation.driver_wiggle import animate_wiggle_bones
from infinigen.assets.creatures.util.creature_util import offset_center

from infinigen.assets.utils.tag import tag_object, tag_nodegroup

from infinigen.assets.materials import fish_eye_shader
from infinigen.assets.creatures.fish import * #fin_params, fish_postprocessing, fish_fin_cloth_sim_params, fish_swim_params, animate_fish_swim


def handfish_genome():
    temp_dict = defaultdict(lambda: 0.001, {'body_handfish': 0.95})
    body_params = parts.generic_nurbs.NurbsBody(
        prefix='body_handfish', tags=['body'], var=U(0.3, 1),
        temperature=temp_dict,
        shoulder_ik_ts=[0.0, 0.4, 0.7, 1.0],
        n_bones=15,
        rig_reverse_skeleton=True)
    body = genome.part(body_params)

    # Positions (u, v, radius)
    dorsal_fin1_coord = (U(0.45, 0.6), 1.0, U(0.6, 0.8))
    dorsal_fin2_coord = (U(0.25, 0.45), 1.0, U(0.6, 0.8))
    pectoral_fin_coord = (0.9, 0.2, 1.0) # Front fin
    hind_fin_coord = (U(0.3, 0.4), N(36, 1)/180, .9) #(U(0.2, 0.3), N(36, 5)/180, .9)
    hand_fin_coord = (0.60, 75/180, 0.6)
    eye_coord = (0.9, 0.6, 0.9)

    pectoral_params = fin_params((0.05, 0.09, 0.08))
    hind_fin_params = fin_params((0.06, 0.2, 0.2))
    tail_params = fin_params((0.1, 0.1, 0.35))
    tail_params['RoundWeight'] = 0.8
    fish_hand_params = fin_params((0.08, 0.08, 0.10))
    fish_hand_params['RoundWeight'] = 0.5

    # Dorsal Fins
    for fin_coord in [dorsal_fin1_coord, dorsal_fin2_coord]:
        dorsal_fin = parts.ridged_fin.FishFin(fin_params((U(0.3, 0.5), 0.5, 0.2), dorsal=True), rig=False)
        genome.attach(genome.part(dorsal_fin), body, coord=fin_coord, joint=Joint(rest=(0, -100, 0)))

    rot = lambda r: np.array((20, r, -205)) # todo: add this back. + N(0, 7, 3)

    # Pectoral Fins - front fin
    pectoral_fin = parts.ridged_fin.FishFin(pectoral_params) #(0.07, 0.1, 0.20)))
    for side in [1, -1]:
        genome.attach(genome.part(pectoral_fin), body, coord=pectoral_fin_coord,
            joint=Joint(rest=(60, 35, 45)), side=side)

    # Hind Fin - Small towards the back
    hind_fin = parts.ridged_fin.FishFin(hind_fin_params) #(0.1, 0.5, 0.3)
    for side in [-1, 1]:
        genome.attach(genome.part(hind_fin), body, coord=hind_fin_coord, joint=Joint(rest=(-30, 120, -15)), side=side) #(20, r, -205)

    # Tail Fin
    angle = U(170, 210)
    tail_fin = parts.ridged_fin.FishFin(tail_params, rig=False)
    for vdir in [-1, 1]:
        genome.attach(genome.part(tail_fin), body, coord=(0.1, .1, 0), joint=Joint((0, -angle * vdir, 0)))

    # Hand
    splay = clip_gaussian(130, 7, 90, 130) / 180
    shoulder_t = clip_gaussian(0.12, 0.05, 0.08, 0.12)
    params = parts.leg.FishHand().sample_params()
    shoulder_bounds = np.array([[-20, -20, -20], [20, 20, 20]])
    fish_hand_fin = parts.ridged_fin.FishFin(fish_hand_params, rig=False) # foot_fac
    fish_hand = parts.leg.FishHand(params=params) # backleg_fac
    for side in [-1, 1]:
        #back_leg = genome.attach(genome.part(foot_fac), genome.part(backleg_fac), coord=(0.9, 0, 0), joint=Joint(rest=(0, 20, 50)))
        arm = genome.attach(genome.part(fish_hand_fin), genome.part(fish_hand), coord=(0.9, .5, .5), joint=Joint(rest=(90, -60, 130)))
        genome.attach(arm, body, coord=hand_fin_coord,
            joint=Joint(rest=(120, 40, U(140, 160))), #, bounds=shoulder_bounds),
            rotation_basis='global', side=side)#, smooth_rad=0.06)#, bridge_rad=0.1)



    eye_fac = parts.eye.MammalEye({'Eyelids': True, 'Radius': N(0.024, 0.01)})
    for side in [-1, 1]:
        genome.attach(genome.part(eye_fac), body, coord=eye_coord,
            joint=Joint(rest=(0,0,0)), side=side, rotation_basis='normal')

    return genome.CreatureGenome(
        parts=body,
        postprocess_params=dict(
            cloth=fish_fin_cloth_sim_params(),
            anim=fish_swim_params(),
            surface_registry=[
                (infinigen.assets.materials.handfishbody, 1),
            ]
        )
    )

#@gin.configurable
@gin.configurable
class HandfishFactory(AssetFactory):

    max_distance = 40

    def __init__(self,
                 factory_seed=None,
                 bvh=None, coarse=False,
                 animation_mode=None,
                 species_variety=None,
                 clothsim_skin: bool = False,
                 **_
    ):
        super().__init__(factory_seed, coarse)
        self.bvh = bvh
        self.animation_mode = animation_mode
        self.clothsim_skin = clothsim_skin

        with FixedSeed(factory_seed):
            self.species_genome = handfish_genome()
            self.species_variety = 0

    def create_asset(self, i, **kwargs):

        instance_genome = genome.interp_genome(self.species_genome, fish_genome(), self.species_variety)

        root, parts = creature.genome_to_creature(instance_genome, name=f'handfish({self.factory_seed}, {i})')
        offset_center(root, x=True, z=False)

        # Force material consistency across a whole species of fish
        # TODO: Replace once Generator class is stnadardized
        def seeded_fish_postprocess(*args, **kwargs):
            with FixedSeed(self.factory_seed):
                fish_postprocessing(*args, handfish=True, **kwargs)

        joined, extras, arma, ik_targets = joining.join_and_rig_parts(
            root, parts, instance_genome, rigging=(self.animation_mode is not None), rig_before_subdiv=True,
            postprocess_func=seeded_fish_postprocess, adapt_mode='subdivide', **kwargs)
        if self.animation_mode is not None and arma is not None:
            if self.animation_mode == 'idle' or self.animation_mode == 'roam':
                animate_fish_swim(arma, instance_genome.postprocess_params['anim'])
            else:
                raise ValueError(f'Unrecognized {self.animation_mode=}')

        if self.clothsim_skin:
            joined = simulate_fish_cloth(joined, extras, instance_genome.postprocess_params['cloth'])
        else:
            joined = butil.join_objects([joined] + extras)
            joined.parent = root

        root.scale = [U(.08, .12)] * 3
        butil.apply_transform(root)

        tag_object(root, 'fish')

        return root


@gin.configurable

class HandfishSchoolFactory(BoidSwarmFactory):
    @gin.configurable
    def fish_school_params(self):

        boids_settings = dict(
            use_flight = True,
            use_land = False,
            use_climb = False,

            rules = [
                dict(type='SEPARATE'),
                dict(type='GOAL'),
                dict(type='FLOCK'),
            ],

            air_speed_max = U(0.1, 0.7),
            air_acc_max = U(0.7, 1),
            air_personal_space = 2, #U(0.15, 2),
            bank = 0, # fish dont tip over / roll
            pitch = 0.4, #
            rule_fuzzy = U(0.6, 0.9)
        )

        return dict(
            particle_size=0.05, #U(0.1, 0.3),
            size_random=0.0, # U(0.0, 0.1),
            use_rotation_instance=True,
            lifetime=bpy.context.scene.frame_end - bpy.context.scene.frame_start,
            warmup_frames=1, emit_duration=0, # all particles appear immediately
            emit_from='VOLUME',
            mass = 2,
            use_multiply_size_mass=True,
            effect_gravity=0,
            boids_settings=boids_settings
        )

    def __init__(self, factory_seed, bvh=None, coarse=False, handfish=False):
        with FixedSeed(factory_seed):
            settings = self.fish_school_params()
            col = make_asset_collection(HandfishFactory(factory_seed=randint(1e7), animation_mode='idle'), n=5)
        super().__init__(
            factory_seed, child_col=col,
            collider_col=bpy.data.collections.get('colliders'),
            settings=settings, bvh=bvh,
            volume=("uniform", 2, 5),
            coarse=coarse
        )

if __name__ == "__main__":
    import os
    for i in range(1):
        factory = HandfishFactory(i, cloth_sim=True)
        root = factory.spawn_asset(i)
        root.location[0] = i+1 * 3
    import os
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.abspath(os.curdir), "dev_handfish.blend"))

