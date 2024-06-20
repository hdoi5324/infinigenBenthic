# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

import argparse
import logging
from pathlib import Path

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] [%(name)s] [%(levelname)s] | %(message)s',
    datefmt='%H:%M:%S',
    level=logging.WARNING
)

import bpy
import mathutils
from mathutils import Vector
import gin
from numpy.random import uniform, randint

logging.basicConfig(level=logging.INFO)

from infinigen.core.placement import (
    particles, placement, density,
    camera as cam_util,
    split_in_view, factory,
    animation_policy, )

from infinigen.assets.scatters import (
    pebbles, mollusk, lichen, seaweed, coral_reef, jellyfish, urchin, scolymia, urchin_kina, plasticbag
)

from infinigen.assets import (
    monocot,
    rocks,
    creatures,
    lighting,
    weather
)
from infinigen.terrain import Terrain
from infinigen.assets.underwater.colourboard import place_colourboard

from infinigen.core.util import (
    blender as butil,
    logging as logging_util,
    pipeline,
)
from infinigen.core.util.random import random_general
from infinigen.core.util.math import int_hash
from infinigen.core import execute_tasks, surface, init

debug = False
if debug:
    import pydevd_pycharm

    pydevd_pycharm.settrace('localhost', port=52000, stdoutToServer=True, stderrToServer=True)


@gin.configurable
def compose_scene(output_folder, scene_seed, fps=24, **params):
    bpy.context.scene.render.fps = fps
    # Set fps globally
    p = pipeline.RandomStageExecutor(scene_seed, output_folder, params)

    def add_coarse_terrain():
        terrain = Terrain(scene_seed, surface.registry, task='coarse', on_the_fly_asset_folder=output_folder / "assets")
        terrain_mesh = terrain.coarse_terrain()
        density.set_tag_dict(terrain.tag_dict)
        return terrain, terrain_mesh

    terrain, terrain_mesh = p.run_stage('terrain', add_coarse_terrain, use_chance=False, default=(None, None))

    if terrain_mesh is None:
        terrain_mesh = butil.create_noise_plane()
        density.set_tag_dict({})

    terrain_bvh = mathutils.bvhtree.BVHTree.FromObject(terrain_mesh, bpy.context.evaluated_depsgraph_get())

    land_domain = params.get('land_domain_tags')
    underwater_domain = params.get('underwater_domain_tags')
    nonliving_domain = params.get('nonliving_domain_tags')

    def add_boulders(terrain_mesh):
        n_boulder_species = randint(1, params.get("max_boulder_species", 5))
        for i in range(n_boulder_species):
            selection = density.placement_mask(0.05, tag=nonliving_domain, select_thresh=uniform(0.55, 0.6))
            fac = rocks.BoulderFactory(int_hash((scene_seed, i)), coarse=True)
            placement.scatter_placeholders_mesh(terrain_mesh, fac,
                                                overall_density=params.get("boulder_density",
                                                                           uniform(.02, .05)) / n_boulder_species,
                                                selection=selection, altitude=-0.25)

    p.run_stage('boulders', add_boulders, terrain_mesh)

    def camera_preprocess():
        camera_rigs = cam_util.spawn_camera_rigs()
        scene_preprocessed = cam_util.camera_selection_preprocessing(terrain, terrain_mesh)
        return camera_rigs, scene_preprocessed

    camera_rigs, scene_preprocessed = p.run_stage('camera_preprocess', camera_preprocess, use_chance=False)

    bbox = terrain.get_bounding_box() if terrain is not None else butil.bounds(terrain_mesh)
    p.run_stage(
        'pose_cameras',
        lambda: cam_util.configure_cameras(camera_rigs, bbox, scene_preprocessed),
        use_chance=False
    )

    p.run_stage(
        'configure_camera_parameters',
        lambda: cam_util.set_camera_parameters(camera_rigs),
        use_chance=False
    )

    # todo: use configuration for setting up lights
    # Set location/rotation of lights to the same as the camera rig and configure lights
    p.run_stage(
        'setup_camera_lights',
        lambda: cam_util.configure_camera_lights(camera_rigs),
        use_chance=False
    )

    cam = cam_util.get_camera(0, 0)

    p.run_stage('lighting', lighting.sky_lighting.add_lighting, cam, use_chance=False)

    # determine a small area of the terrain for the creatures to run around on
    # must happen before camera is animated, as camera may want to follow them around
    terrain_center, *_ = split_in_view.split_inview(terrain_mesh, cam=cam,
                                                    start=0, end=0, outofview=False, vis_margin=5,
                                                    dist_max=params["center_distance"],
                                                    hide_render=True, suffix='center')
    deps = bpy.context.evaluated_depsgraph_get()
    terrain_center_bvh = mathutils.bvhtree.BVHTree.FromObject(terrain_center, deps)

    pois = []  # objects / points of interest, for the camera to look at

    # Crustaceans
    def add_ground_creatures(target):
        fac_class = creatures.CrustaceanFactory  # sample_registry(params['ground_creature_registry'])
        fac = fac_class(int_hash((scene_seed, 0)), bvh=terrain_bvh, animation_mode='idle')
        n = params.get('max_ground_creatures', randint(1, 4))
        selection = density.placement_mask(select_thresh=0, tag=underwater_domain, altitude_range=(-0.5, 0.5)) \
            if fac_class is creatures.CrabFactory else 1
        col = placement.scatter_placeholders_mesh(target, fac, num_placeholders=n, overall_density=1,
                                                  selection=selection, altitude=0.2)
        return list(col.objects)

    pois += p.run_stage('ground_creatures', add_ground_creatures, target=terrain_center, default=[])

    p.run_stage('animate_cameras', lambda: cam_util.animate_cameras(
        camera_rigs, scene_preprocessed, pois=pois, policy_registry=animation_policy.AnimPolicyMowTheLawn),
                use_chance=False)

    with logging_util.Timer('Compute coarse terrain frustrums'):
        terrain_inview, *_ = split_in_view.split_inview(
            terrain_mesh, verbose=True, outofview=False, print_areas=True,
            cam=cam, vis_margin=2, dist_max=params['inview_distance'], hide_render=True, suffix='inview'
        )
        terrain_near, *_ = split_in_view.split_inview(
            terrain_mesh, verbose=True, outofview=False, print_areas=True,
            cam=cam, vis_margin=2, dist_max=params['near_distance'], hide_render=True, suffix='near'
        )

        collider = butil.modify_mesh(butil.deep_clone_obj(terrain_near), 'COLLISION', apply=False, show_viewport=True)
        collider.name = collider.name + '.collider'
        collider.collision.use_culling = False
        collider_col = butil.get_collection('colliders')
        butil.put_in_collection(collider, collider_col)

        butil.modify_mesh(terrain_near, 'SUBSURF', levels=2, apply=True)

        deps = bpy.context.evaluated_depsgraph_get()
        terrain_inview_bvh = mathutils.bvhtree.BVHTree.FromObject(terrain_inview, deps)

    def add_rocks(target):
        selection = density.placement_mask(scale=0.15, select_thresh=0.4,
                                           normal_thresh=0.7, return_scalar=True, tag=nonliving_domain)
        _, rock_col = pebbles.apply(target, selection=selection)
        return rock_col

    p.run_stage('rocks', add_rocks, terrain_mesh)

    def add_corals(target):
        vertical_faces = density.placement_mask(scale=0.15, select_thresh=uniform(.44, .48))
        coral_reef.apply(target, n=3, selection=vertical_faces, tag=underwater_domain,
                         density=params.get('coral_density', 1.5))
        horizontal_faces = density.placement_mask(scale=.15, normal_thresh=-.4, normal_thresh_high=.4)
        coral_reef.apply(target, selection=horizontal_faces, n=3, horizontal=True, tag=underwater_domain,
                         density=params.get('horizontal_coral_density', 1.5))

    p.run_stage('corals', add_corals, terrain_inview)

    def add_kelp(terrain_mesh):
        fac = monocot.KelpMonocotFactory(int_hash((scene_seed, 0)), coarse=True)
        selection = density.placement_mask(scale=0.01, tag=underwater_domain, select_thresh=.3)
        placement.scatter_placeholders_mesh(terrain_mesh, fac, altitude=-0.05,
                                            overall_density=params.get('kelp_density', uniform(.1, .3)),
                                            selection=selection, distance_min=5)

    p.run_stage('kelp', add_kelp, terrain_inview)

    p.run_stage('lichen', lambda: lichen.apply(terrain_inview,
                                               selection=density.placement_mask(scale=0.05, select_thresh=.5,
                                                                                normal_thresh=0.0,
                                                                                tag=underwater_domain),
                                               density=random_general(('uniform', 20, 100))))
    p.run_stage('mollusk', lambda: mollusk.apply(terrain_inview,
                                                 selection=density.placement_mask(scale=0.04, select_thresh=.3,
                                                                                  normal_thresh=0.0,
                                                                                  tag=underwater_domain),
                                                 density=random_general(('uniform', 1, 10))))
    p.run_stage('seaweed', lambda: seaweed.apply(terrain_inview,
                                                 selection=density.placement_mask(scale=0.05, select_thresh=.55,
                                                                                  normal_thresh=0.4,
                                                                                  tag=underwater_domain)))

    urchin_density = random_general(('uniform', .5, 4))  # no per square metre
    urchin_select_threshold = uniform(0.0, 0.1)  # Lower covers more of the terrain_inview

    p.run_stage('urchin', lambda: urchin.apply(terrain_inview,
                                               selection=density.placement_mask(scale=0.05,
                                                                                select_thresh=urchin_select_threshold,
                                                                                normal_thresh=0.0,
                                                                                tag=underwater_domain),
                                               density=urchin_density))

    p.run_stage('urchinkina', lambda: urchin_kina.apply(terrain_inview,
                                                        selection=density.placement_mask(scale=0.05,
                                                                                         select_thresh=urchin_select_threshold,
                                                                                         normal_thresh=0.0,
                                                                                         tag=underwater_domain),
                                                        density=urchin_density))

    def add_fish_school():
        n = random_general(params.get("max_fish_schools", 3))
        for i in range(n):
            selection = density.placement_mask(0.1, select_thresh=0, tag=underwater_domain)
            fac = creatures.FishSchoolFactory(randint(1e7), bvh=terrain_inview_bvh)
            col = placement.scatter_placeholders_mesh(terrain_near, fac, selection=selection,
                                                      overall_density=1, num_placeholders=1, altitude=1.8)
            placement.populate_collection(fac, col)

    p.run_stage('fish_school', add_fish_school, default=[])

    def add_handfish():
        selection = density.placement_mask(scale=0.05, select_thresh=uniform(0.1, 0.3), tag=underwater_domain)
        fac = creatures.HandfishSchoolFactory(randint(1e7 + 55), bvh=terrain_inview_bvh)
        col = placement.scatter_placeholders_mesh(terrain_near, fac, selection=selection,
                                                  overall_density=1, num_placeholders=1, altitude=.1)
        placement.populate_collection(fac, col)

    p.run_stage('handfish', add_handfish, default=[])

    p.run_stage('scolymia', lambda: scolymia.apply(terrain_inview,
                                                   selection=density.placement_mask(scale=0.05, select_thresh=.5,
                                                                                    tag=underwater_domain)))
    p.run_stage('jellyfish', lambda: jellyfish.apply(terrain_inview,
                                                     selection=density.placement_mask(scale=0.05, select_thresh=.5,
                                                                                      tag=underwater_domain)))

    p.run_stage('colourboard', lambda: place_colourboard(cam.parent, terrain_bvh, n=3, alt=0.02, dist_range=(0, 2)))

    def add_plastic_bags(target):
        selection = density.placement_mask(scale=0.1, select_thresh=0.52, normal_thresh=0.7,
                                           tag=nonliving_domain)
        plasticbag.apply(target, selection=selection)

    p.run_stage('plasticbag', add_plastic_bags, terrain_near)

    def add_marine_snow_particles():
        return particles.particle_system(
            emitter=butil.spawn_cube(location=Vector(), size=30),
            subject=factory.make_asset_collection(weather.particles.DustMoteFactory(scene_seed), 5),
            settings=particles.marine_snow_setting())

    particle_systems = [
        p.run_stage('marine_snow_particles', add_marine_snow_particles),
    ]

    for emitter, system in filter(lambda s: s is not None, particle_systems):
        with logging_util.Timer(f"Baking particle system"):
            butil.constrain_object(emitter, "COPY_LOCATION", use_offset=True, target=cam.parent)
            particles.bake(emitter, system)
        butil.put_in_collection(emitter, butil.get_collection('particles'))

    p.save_results(output_folder / 'pipeline_coarse.csv')
    return terrain, terrain_mesh


def main(args):
    scene_seed = init.apply_scene_seed(args.seed)
    init.apply_gin_configs(
        configs=args.configs,
        overrides=args.overrides,
        configs_folder='infinigen_examples/configs',
        mandatory_folders=['infinigen_examples/configs/scene_types'],
    )

    execute_tasks.main(
        compose_scene_func=compose_scene,
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        task=args.task,
        task_uniqname=args.task_uniqname,
        scene_seed=scene_seed
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_folder', type=Path)
    parser.add_argument('--input_folder', type=Path, default=None)
    parser.add_argument('-s', '--seed', default=None, help="The seed used to generate the scene")
    parser.add_argument('-t', '--task', nargs='+', default=['coarse'],
                        choices=['coarse', 'populate', 'fine_terrain', 'ground_truth', 'render', 'mesh_save'])
    parser.add_argument('-g', '--configs', nargs='+', default=['base'],
                        help='Set of config files for gin (separated by spaces) '
                             'e.g. --gin_config file1 file2 (exclude .gin from path)')
    parser.add_argument('-p', '--overrides', nargs='+', default=[],
                        help='Parameter settings that override config defaults '
                             'e.g. --gin_param module_1.a=2 module_2.b=3')
    parser.add_argument('--task_uniqname', type=str, default=None)
    parser.add_argument('-d', '--debug', action="store_const", dest="loglevel", const=logging.DEBUG,
                        default=logging.INFO)

    args = init.parse_args_blender(parser)
    logging.getLogger("infinigen").setLevel(args.loglevel)

    main(args)
