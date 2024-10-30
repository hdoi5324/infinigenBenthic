# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors:
# - Alexander Raistrick: FishSchoolFactory, basic version of FishFactory, anim & simulation
# - Mingzhe Wang: Fin placement


from collections import defaultdict

import bpy
import gin
import numpy as np
import random
from numpy.random import uniform as U, normal as N, randint

import infinigen.assets.materials.scale
import infinigen.assets.materials.handfishbody
import infinigen.assets.materials.fishbody
from infinigen.assets.materials import eyeball
from infinigen.core import surface

from infinigen.core.placement.factory import AssetFactory, make_asset_collection

from infinigen.assets.objects.creatures.util import genome
from infinigen.assets.objects.creatures import parts
from infinigen.assets.objects.creatures.util import creature, joining
from infinigen.assets.objects.creatures.util.boid_swarm import BoidSwarmFactory

from infinigen.core.util import blender as butil
from infinigen.core.util.math import clip_gaussian, FixedSeed
from infinigen.core.util.random import random_general as rg
from infinigen.assets.objects.creatures.util.animation.driver_wiggle import animate_wiggle_bones
from infinigen.assets.objects.creatures.util.creature_util import offset_center

from infinigen.core.tagging import tag_object

from infinigen.assets.materials import fish_eye_shader, handfishfin
from infinigen.assets.objects.creatures.fish import fin_params, fish_fin_cloth_sim_params, fish_genome, simulate_fish_cloth
from infinigen.core.placement import detail
from infinigen.assets.objects.creatures.util.genome import Joint


def handfish_genome():
    temp_dict = defaultdict(lambda: .2, {'body_handfish': 0.95})
    body_params = parts.generic_nurbs.NurbsBody(
        prefix='body_handfish', tags=['body'], var=U(0.3, 1),
        temperature=temp_dict,
        shoulder_ik_ts=[0.0, 0.3, 0.7, 1.0],
        n_bones=15,
        rig_reverse_skeleton=True)
    body = genome.part(body_params)

    # Positions (u, v, radius)

    # Dorsal Fins
    dorsal_fin1_coord = (U(0.6, 0.75), 1.0, U(0.7, 0.95))
    dorsal_fin_1 = parts.ridged_fin.FishFin(fin_params((U(0.4, 0.6), 0.5, U(0.1, 0.2)), dorsal=True), 
                                          rig=False)
    genome.attach(genome.part(dorsal_fin_1), body, coord=dorsal_fin1_coord, joint=Joint(rest=(0, -90, 0)))

    dorsal_fin2_coord = (U(0.35, 0.45), 1.0, U(0.7, 0.9))
    if random.random() > 0.0:
        width = U(0.06, 0.08)
        dorsal_fin_2_params = fin_params((width, 4.5, .1), dorsal=False)
        dorsal_fin_2 = parts.ridged_fin.FishFin(dorsal_fin_2_params, rig=False)
        genome.attach(genome.part(dorsal_fin_2), body, coord=dorsal_fin2_coord, joint=Joint(rest=(0, -40, 180)))

    # Pectoral Fins - front fin
    pectoral_fin_coord = (0.9, .15, .9) 
    pectoral_params = fin_params((0.07, 4.0, 0.1), dorsal=True)
    pectoral_params['RoundingWeight'] = 1.0
    if random.random() > 0.0:
        pectoral_fin = parts.ridged_fin.FishFin(pectoral_params) #(0.07, 0.1, 0.20)))
        for side in [-1, 1]:
            genome.attach(genome.part(pectoral_fin), body, coord=pectoral_fin_coord,
                joint=Joint(rest=(120,90,90)), side=side) #(95,95,30)

    # Tail Fin
    tail_params = fin_params((0.1, 0.1, 0.3))
    tail_params['RoundWeight'] = 0.8
    angle = U(150, 200)
    tail_fin = parts.ridged_fin.FishFin(tail_params, rig=False)
    for vdir in [-1, 1]:
        genome.attach(genome.part(tail_fin), body, coord=(0.1, .1, 0), joint=Joint((0, -angle * vdir, 0)))

    # Hand (Arm)2
    fish_hand_fin_params = fin_params((0.07, 1.0, 0.07), dorsal=True)
    fish_hand_fin = parts.ridged_fin.FishFin(fish_hand_fin_params, rig=False) # foot_fac

    hand_fin_arm_params = infinigen.assets.objects.creatures.parts.leg.FishHand().sample_params()
    hand_fin_arm = infinigen.assets.objects.creatures.parts.leg.FishHand(params=hand_fin_arm_params) # backleg_fac
    hand_fin_arm_coord = (0.70, 90/180, .7) # good

    for side in [-1, 1]:
        arm = genome.attach(genome.part(fish_hand_fin), genome.part(hand_fin_arm), coord=(.9, 0.0, 0.4), joint=Joint(rest=(0,-45,50)), rotation_basis='normal') #, coord=(0.9, .5, .9), joint=Joint(rest=(90, -60, 130)))
        genome.attach(arm, body, coord=hand_fin_arm_coord,
            joint=Joint(rest=(U(-20, -80), U(180,200), U(5,-20))), #, bounds=shoulder_bounds), 120, 40, U(140, 160))
            side=side)#, smooth_rad=0.06)#, bridge_rad=0.1)

    # Eye
    eye_coord = (0.9, 0.6, 1.0)
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
                (infinigen.assets.materials.handfishbody, 3),
            ]
        )
    )

#@gin.configurable
@gin.configurable
class HandfishFactory(AssetFactory):
    max_distance = 40

    def __init__(
        self,
        factory_seed=None,
        bvh=None,
        coarse=False,
        animation_mode='idle',
        species_variety=None,
        clothsim_skin: bool = False,
        scale: tuple = ("uniform", 0.07, 0.12),
        **_,
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

        root, parts = creature.genome_to_creature(
            instance_genome, name=f"handfish({self.factory_seed}, {i})"
        )
        offset_center(root, x=True, z=False)

        # Force material consistency across a whole species of fish
        # TODO: Replace once Generator class is stnadardized
        def seeded_fish_postprocess(*args, **kwargs):
            with FixedSeed(self.factory_seed):
                fish_postprocessing(*args, **kwargs)

        joined, extras, arma, ik_targets = joining.join_and_rig_parts(
            root,
            parts,
            instance_genome,
            rigging=(self.animation_mode is not None),
            rig_before_subdiv=True,
            postprocess_func=seeded_fish_postprocess,
            adapt_mode="subdivide",
            **kwargs,
        )
        if self.animation_mode is not None and arma is not None:
            if self.animation_mode == "idle" or self.animation_mode == "roam":
                animate_fish_swim(arma, instance_genome.postprocess_params["anim"])
            else:
                raise ValueError(f"Unrecognized {self.animation_mode=}")


        if self.clothsim_skin:
            joined = simulate_fish_cloth(
                joined, extras, instance_genome.postprocess_params["cloth"]
            )
        else:
            joined = butil.join_objects([joined] + extras)
            joined.parent = root

            scale = [rg(self.scale)] * 3
            for o in list(root.children):
                o.scale = scale
                butil.apply_transform(o, scale=True)

        tag_object(root, 'handfish')

        return root

def animate_fish_swim(arma, params):
    spine = [b for b in arma.pose.bones if "Body" in b.name]
    fin_bones = [b for b in arma.pose.bones if "extra_bone(Fin" in b.name]
    hand_bones = [b for b in arma.pose.bones if "Hand" in b.name]

    global_offset = U(0, 1000)  # so swimming animations dont sync across fish
    animate_wiggle_bones(
        arma=arma,
        bones=spine,
        off=global_offset,
        mag_deg=params["swim_mag"],
        freq=params["swim_freq"],
        wavelength=U(0.5, 2),
    )
    v = params["flipper_var"]
    for b in fin_bones + hand_bones:
        animate_wiggle_bones(
            arma=arma,
            bones=[b],
            off=global_offset + U(0, 1),
            mag_deg=params["flipper_mag"] * N(1, v),
            freq=params["flipper_mag"] * N(1, v),
        )


def fish_postprocessing(body_parts, extras, params):
    def get_extras(k):
        return [o for o in extras if k in o.name]

    main_template = surface.registry.sample_registry(params['surface_registry'])
    main_template.apply(body_parts + get_extras('BodyExtra'))

    mat = body_parts[0].active_material
    spotted = mat is not None and "spotted" in mat.name
    body_parts[0].active_material.name.lower() or U() < 0.1
    handfishfin.apply(get_extras('Fin'), geo_kwargs={"spotted": spotted})

    fish_eye_shader.apply(get_extras('Eyeball'))
    eyeball.apply(get_extras('Eyeball'), shader_kwargs={"coord": "X"})
def fish_swim_params():
    swim_freq = 1 #3 * clip_gaussian(.6, 0.3, 0.1, 2)
    swim_mag = N(120, 3)
    return dict(
        swim_mag=swim_mag,
        swim_freq=swim_freq,
        flipper_freq = 2 * clip_gaussian(1, 0.5, 0.1, 3) * swim_freq,
        flipper_mag = 0.05  * swim_mag,
        flipper_var = U(0, 0.2),
    )


if __name__ == "__main__":
    import os

    bpy.context.scene.frame_end = 5
    bpy.ops.object.delete(use_global=False)

    for i in range(1):
        factory = HandfishFactory(i, clothsim_skin=False, animation_mode='idle')
        root = factory.spawn_asset(i)
        #root.location[0] = i+1 * 3
        #butil.apply_transform(root, loc=True)
    import os
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.abspath(os.curdir), "dev_handfish.blend"))

