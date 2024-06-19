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
from infinigen.core.util.random import random_general as rg
from infinigen.assets.creatures.util.animation.driver_wiggle import animate_wiggle_bones
from infinigen.assets.creatures.util.creature_util import offset_center

from infinigen.assets.utils.tag import tag_object, tag_nodegroup

from infinigen.assets.materials import fish_eye_shader, handfishfin
from infinigen.assets.creatures.fish import fin_params, fish_fin_cloth_sim_params, fish_genome, simulate_fish_cloth
from infinigen.core.placement import detail
from infinigen.assets.creatures.util.genome import Joint, IKParams


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
    pectoral_fin_coord = (0.9, 0.1, .5) # Front fin
    hind_fin_coord = (U(0.3, 0.4), N(36, 1)/180, .9) #(U(0.2, 0.3), N(36, 5)/180, .9)
    hand_fin_coord = (0.60, 75/180, 0.9)
    eye_coord = (0.9, 0.6, 1.0)

    pectoral_params = fin_params((0.06, 0.5, 0.3))
    hind_fin_params = fin_params((0.1, 0.5, 0.3)) # ((0.06, 0.2, 0.9))
    tail_params = fin_params((0.1, 0.1, 0.35))
    tail_params['RoundWeight'] = 0.8
    fish_hand_params = fin_params((0.1, 0.5, 0.2))
    fish_hand_params['RoundWeight'] = 0.8

    # Dorsal Fins
    for fin_coord in [dorsal_fin1_coord, dorsal_fin2_coord]:
        dorsal_fin = parts.ridged_fin.FishFin(fin_params((U(0.3, 0.5), 0.5, 0.2), dorsal=True), rig=False)
        genome.attach(genome.part(dorsal_fin), body, coord=fin_coord, joint=Joint(rest=(0, -100, 0)))

    rot = lambda r: np.array((60, r, 45)) + N(0, 7, 3)

    # Pectoral Fins - front fin
    pectoral_fin = parts.ridged_fin.FishFin(pectoral_params) #(0.07, 0.1, 0.20)))
    for side in [-1, 1]:
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
    params = parts.leg.FishHand().sample_params()
    fish_hand_fin = parts.ridged_fin.FishFin(fish_hand_params) # foot_fac

    fish_hand = parts.leg.FishHand(params=params) # backleg_fac
    for side in [-1, 1]:
        arm = genome.attach(genome.part(fish_hand_fin), genome.part(fish_hand), coord=(0.8, 0, 0.2), joint=Joint(rest=(30, -70, -40)), rotation_basis='normal') #, coord=(0.9, .5, .9), joint=Joint(rest=(90, -60, 130)))
        genome.attach(arm, body, coord=hand_fin_coord,
            joint=Joint(rest=(120, 40, U(140, 160))), #, bounds=shoulder_bounds),
            rotation_basis='global', side=side)#, smooth_rad=0.06)#, bridge_rad=0.1)


    eye_fac = parts.eye.MammalEye({'Eyelids': True, 'Radius': N(0.016, 0.006)})
    for side in [-1, 1]:
        genome.attach(genome.part(eye_fac), body, coord=eye_coord,
            joint=Joint(rest=(0,0,0)), side=side, rotation_basis='normal')

    return genome.CreatureGenome(
        parts=body,
        postprocess_params=dict(
            cloth=fish_fin_cloth_sim_params(),
            anim=fish_swim_params(),
            surface_registry=[
                (infinigen.assets.materials.handfishbody, 100),
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
                 animation_mode='idle',
                 species_variety=None,
                 clothsim_skin: bool = False,
                 scale: tuple = ("uniform", 0.09, 0.15),
                 **_
    ):
        super().__init__(factory_seed, coarse)
        self.bvh = bvh
        self.animation_mode = animation_mode
        self.clothsim_skin = clothsim_skin
        self.scale = scale

        with FixedSeed(factory_seed):
            self.species_genome = handfish_genome()
            self.species_variety = 0

    def asset_parameters(self, distance: float, vis_distance: float) -> dict:
        # Optionally, override to determine the **params input of create_asset w.r.t. camera distance
        return {'face_size': detail.target_face_size(distance), 'distance': distance,
                'vis_distance': vis_distance}

    def create_asset(self, i, **kwargs):

        instance_genome = genome.interp_genome(self.species_genome, fish_genome(), self.species_variety)

        root, parts = creature.genome_to_creature(instance_genome, name=f'handfish({self.factory_seed}, {i})')

        offset_center(root, x=True, z=False)

        # Force material consistency across a whole species of fish
        # TODO: Replace once Generator class is stnadardized
        def seeded_fish_postprocess(*args, **kwargs):
            with FixedSeed(self.factory_seed):
                fish_postprocessing(*args, **kwargs)

        joined, extras, arma, ik_targets = joining.join_and_rig_parts(
            root, parts, instance_genome, rigging=(self.animation_mode is not None), rig_before_subdiv=True,
            postprocess_func=seeded_fish_postprocess, adapt_mode='subdivide', **kwargs)

        if self.animation_mode is not None and arma is not None:
            if self.animation_mode == 'idle' or self.animation_mode == 'roam':
                animate_fish_swim(arma, instance_genome.postprocess_params['anim'])
            else:
                raise ValueError(f'Unrecognized {self.animation_mode=}')

        if self.clothsim_skin:
            _ = simulate_fish_cloth(joined, extras, instance_genome.postprocess_params['cloth'])
        else:
            joined = butil.join_objects([joined] + extras)
            joined.parent = root

            scale = [rg(self.scale)] * 3
            for o in list(root.children):
                o.scale = scale
                butil.apply_transform(o, scale=True)

        tag_object(root, 'fish')

        return root

def animate_fish_swim(arma, params):

    spine = [b for b in arma.pose.bones if 'Body' in b.name]
    fin_bones = [b for b in arma.pose.bones if 'extra_bone(Fin' in b.name]
    hand_bones = [b for b in arma.pose.bones if 'Hand' in b.name]

    global_offset = U(0, 1000) # so swimming animations dont sync across fish
    animate_wiggle_bones(
        arma=arma, bones=spine,
        off=global_offset,
        mag_deg=params['swim_mag'], freq=params['swim_freq'], wavelength=U(0.5, 2))
    v = params['flipper_var']
    for b in fin_bones + hand_bones:
        animate_wiggle_bones(
            arma=arma, bones=[b], off=global_offset+U(0, 1),
            mag_deg=params['flipper_mag']*N(1, v),
            freq=params['flipper_mag']*N(1, v))


def fish_postprocessing(body_parts, extras, params):

    get_extras = lambda k: [o for o in extras if k in o.name]
    main_template = surface.registry.sample_registry(params['surface_registry'])
    main_template.apply(body_parts + get_extras('BodyExtra'))

    handfishfin.apply(get_extras('Fin'))

    fish_eye_shader.apply(get_extras('Eyeball'))
    eyeball.apply(get_extras('Eyeball'), shader_kwargs={"coord": "X"})
def fish_swim_params():
    swim_freq = 3 * clip_gaussian(.6, 0.3, 0.1, 2)
    swim_mag = N(30, 3)
    return dict(
        swim_mag=swim_mag,
        swim_freq=swim_freq,
        flipper_freq = 2 * clip_gaussian(1, 0.5, 0.1, 3) * swim_freq,
        flipper_mag = 0.35 * N(1, 0.1) * swim_mag,
        flipper_var = U(0, 0.2),
    )
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
                dict(type='AVERAGE_SPEED'),
            ],

            air_speed_max = U(.3, .5),
            air_acc_max = U(0.7, 1),
            air_personal_space = U(1.5, 2),
            bank = 0, # fish dont tip over / roll
            pitch = 0.1, #
            rule_fuzzy = U(0.6, 0.9)
        )

        return dict(
            particle_size=U(0.09, .14),
            size_random=U(0.1, 0.3),

            use_rotation_instance=True,

            lifetime=bpy.context.scene.frame_end - bpy.context.scene.frame_start,
            warmup_frames=1, emit_duration=0, # all particles appear immediately
            emit_from='VOLUME',
            mass = 2,
            use_multiply_size_mass=True,
            effect_gravity=0,

            boids_settings=boids_settings
        )

    def __init__(self, factory_seed, bvh=None, coarse=False):
        with FixedSeed(factory_seed):
            settings = self.fish_school_params()
            col = make_asset_collection(HandfishFactory(factory_seed=randint(1e7),
                                                    animation_mode='idle',
                                                    scale=1.0, n=3))
        super().__init__(
            factory_seed, child_col=col,
            collider_col=bpy.data.collections.get('colliders'),
            settings=settings, bvh=bvh,
            volume=("uniform", 2, 5),
            coarse=coarse
        )

if __name__ == "__main__":
    import os

    bpy.context.scene.frame_end = 5
    bpy.ops.object.delete(use_global=False)

    for i in range(1):
        factory = HandfishFactory(i, clothsim_skin=True, animation_mode='idle')
        root = factory.spawn_asset(i)
        #root.location[0] = i+1 * 3
        #butil.apply_transform(root, loc=True)
    import os
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.abspath(os.curdir), "dev_handfish.blend"))

