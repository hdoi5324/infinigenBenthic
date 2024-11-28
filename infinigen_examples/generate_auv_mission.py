# Copyright (C) 2023, Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

import argparse
import itertools
import logging
from pathlib import Path

import bpy
import gin
import mathutils
from mathutils import Vector
from numpy.random import randint, uniform

# ruff: noqa: E402
# NOTE: logging config has to be before imports that use logging
logging.basicConfig(
    format="[%(asctime)s.%(msecs)03d] [%(module)s] [%(levelname)s] | %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

from infinigen.assets import fluid, lighting, weather
from infinigen.assets.materials import (
    atmosphere_light_haze,
    chunkyrock,
    cobble_stone,
    cracked_ground,
    dirt,
    ice,
    lava,
    mountain,
    mud,
    sand,
    sandstone,
    snow,
    soil,
    stone,
    water,
)
from infinigen.assets.objects import (
    cactus,
    cloud,
    creatures,
    leaves,
    monocot,
    particles,
    rocks,
    trees,
)
from infinigen.assets.scatters import (
    chopped_trees,
    coral_reef,
    decorative_plants,
    fern,
    flowerplant,
    grass,
    ground_leaves,
    ground_mushroom,
    ground_twigs,
    ivy,
    jellyfish,
    lichen,
    mollusk,
    monocots,
    moss,
    pebbles,
    pine_needle,
    pinecone,
    seashells,
    seaweed,
    slime_mold,
    snow_layer,
    urchin,
#    urchin_kina, #todo: migrate from octoq
#    plasticbag,
#    cocoimageplane,

)
#####from infinigen.assets.objects.underwater.colourboard import place_colourboard #todo: migrate from octo
from infinigen.assets.scatters.utils.selection import scatter_lower, scatter_upward
from infinigen.core import execute_tasks, init, surface
from infinigen.core.placement import camera as cam_util
from infinigen.core.placement.camera_utility import set_camera_parameters
from infinigen.core.placement import density, placement, split_in_view
from infinigen.core.util import blender as butil
from infinigen.core.util import logging as logging_util
from infinigen.core.util import pipeline
from infinigen.core.util.imu import save_imu_tum_files
from infinigen.core.util.math import FixedSeed, int_hash
from infinigen.core.util.organization import Tags, Task
from infinigen.core.util.pipeline import RandomStageExecutor
from infinigen.core.util.random import random_general, sample_registry
from infinigen.terrain import Terrain

logger = logging.getLogger(__name__)


debug = False
if debug:
    import pydevd_pycharm

    pydevd_pycharm.settrace('localhost', port=52000, stdoutToServer=True, stderrToServer=True)


@gin.configurable
def compose_nature(output_folder, scene_seed, fps=24, **params):
    bpy.context.scene.render.fps = fps
    # Set fps globally
    p = pipeline.RandomStageExecutor(scene_seed, output_folder, params)

    def add_coarse_terrain():
        terrain = Terrain(
            scene_seed,
            surface.registry,
            task="coarse",
            on_the_fly_asset_folder=output_folder / "assets",
        )
        terrain_mesh = terrain.coarse_terrain()
        density.set_tag_dict(terrain.tag_dict)
        return terrain, terrain_mesh

    terrain, terrain_mesh = p.run_stage(
        "terrain", add_coarse_terrain, use_chance=False, default=(None, None)
    )

    if terrain_mesh is None:
        terrain_mesh = butil.create_noise_plane()
        density.set_tag_dict({})

    scene_bvh = mathutils.bvhtree.BVHTree.FromObject(
        terrain_mesh, bpy.context.evaluated_depsgraph_get()
    )

    land_domain = params.get("land_domain_tags")
    underwater_domain = params.get("underwater_domain_tags")
    nonliving_domain = params.get("nonliving_domain_tags")



    def add_boulders(terrain_mesh):
        n_boulder_species = randint(1, params.get("max_boulder_species", 5))
        for i in range(n_boulder_species):
            selection = density.placement_mask(
                0.05, tag=nonliving_domain, select_thresh=uniform(0.35, 0.6)
            )
            fac = rocks.BoulderFactory(int_hash((scene_seed, i)), coarse=True)
            placement.scatter_placeholders_mesh(
                terrain_mesh,
                fac,
                overall_density=params.get("boulder_density", uniform(0.02, 0.05))
                / n_boulder_species,
                selection=selection,
                altitude=-0.25,
            )

    p.run_stage("boulders", add_boulders, terrain_mesh)

    def camera_preprocess():
        camera_rigs = cam_util.spawn_camera_rigs() #todo: do onboard lights later?

        # Set camera lens parameters including distortion
        set_camera_parameters(camera_rigs, parameter_dir=output_folder.parent)
        scene_preprocessed = cam_util.camera_selection_preprocessing(
            terrain,
            terrain_mesh,
            tags_ratio=params.get("camera_selection_tags_ratio"),
            ranges_ratio=params.get("camera_selection_ranges_ratio"),
            anim_criterion_keys=params.get(
                "camera_selection_anim_criterion_keys", False
            ),
        )
        return camera_rigs, scene_preprocessed

    camera_rigs, scene_preprocessed = p.run_stage(
        "camera_preprocess", camera_preprocess, use_chance=False
    )

    bbox = (
        terrain.get_bounding_box()
        if terrain is not None
        else butil.bounds(terrain_mesh)
    )
    p.run_stage(
        "pose_cameras",
        lambda: cam_util.configure_cameras(
            camera_rigs,
            scene_preprocessed,
            init_bounding_box=bbox,
            terrain_mesh=terrain_mesh,
        ),
        use_chance=False,
    )
    primary_cams = [rig.children[0] for rig in camera_rigs]

    # Set location/rotation of lights to the same as the camera rig and configure lights
    p.run_stage(
        'setup_camera_lights',
        lambda: cam_util.configure_camera_lights(camera_rigs),
        use_chance=False
    )

    p.run_stage(
        "lighting",
        lighting.sky_lighting.add_lighting,
        primary_cams[0],
        use_chance=False,
    )

    # determine a small area of the terrain for the creatures to run around on
    # must happen before camera is animated, as camera may want to follow them around
    terrain_center, *_ = split_in_view.split_inview(
        terrain_mesh,
        primary_cams,
        dist_max=params["center_distance"],
        vis_margin=5,
        frame_start=0,
        frame_end=0,
        outofview=False,
        hide_render=True,
        suffix="center",
    )
    deps = bpy.context.evaluated_depsgraph_get()
    mathutils.bvhtree.BVHTree.FromObject(terrain_center, deps)

    pois = []  # objects / points of interest, for the camera to look at

    # Crustaceans
    def add_ground_creatures(target):
        fac_class = creatures.CrustaceanFactory  # sample_registry(params['ground_creature_registry'])
        fac = fac_class(int_hash((scene_seed, 0)), bvh=scene_bvh, animation_mode="idle")
        n = params.get("max_ground_creatures", randint(1, 4))
        selection = (
            density.placement_mask(
                select_thresh=0, tag="beach", altitude_range=(-0.5, 0.5)
            )
            if fac_class is creatures.CrabFactory
            else 1
        )
        col = placement.scatter_placeholders_mesh(
            target,
            fac,
            num_placeholders=n,
            overall_density=1,
            selection=selection,
            altitude=0.2,
        )
        return list(col.objects)

    pois += p.run_stage(
        "ground_creatures", add_ground_creatures, target=terrain_center, default=[]
    )

    def add_handfish(target):
        pois = []
        n_handfish_species = params.get("max_handfish", 5)
        for i in range(n_handfish_species):
            fac = creatures.HandfishFactory(int_hash((scene_seed+i, 0)), bvh=scene_bvh, animation_mode='idle')
            selection = density.placement_mask(
                scale=0.05, tag=underwater_domain, select_thresh=0.4
            )
            col = placement.scatter_placeholders_mesh(
                target,
                fac,
                altitude=uniform(0.015, 0.04),
                overall_density=0.7 / n_handfish_species,
                selection=selection,
                distance_min=1,
            )
            pois += list(col.objects)
        return pois

    pois += p.run_stage('handfish', add_handfish, target=terrain_center, default=[])

    def animate_cameras():
        cam_util.animate_cameras(camera_rigs, bbox, scene_preprocessed, pois=pois)

        frames_folder = output_folder.parent / "frames"
        animated_cams = [cam for cam in camera_rigs if cam.animation_data is not None]
        save_imu_tum_files(frames_folder / "imu_tum", animated_cams)

    p.run_stage(
        "animate_cameras",
        animate_cameras,
        use_chance=False,
    )

    with logging_util.Timer("Compute coarse terrain frustrums"):
        terrain_inview, *_ = split_in_view.split_inview(
            terrain_mesh,
            primary_cams,
            verbose=True,
            outofview=False,
            vis_margin=2,
            dist_max=params["inview_distance"],
            hide_render=True,
            suffix="inview",
        )
        terrain_near, *_ = split_in_view.split_inview(
            terrain_mesh,
            primary_cams,
            verbose=True,
            outofview=False,
            vis_margin=2,
            dist_max=params["near_distance"],
            hide_render=True,
            suffix="near",
        )

        collider = butil.modify_mesh(
            butil.deep_clone_obj(terrain_near),
            "COLLISION",
            apply=False,
            show_viewport=True,
        )
        collider.name = collider.name + ".collider"
        collider.collision.use_culling = False
        collider_col = butil.get_collection("colliders")
        butil.put_in_collection(collider, collider_col)

        butil.modify_mesh(terrain_near, "SUBSURF", levels=2, apply=True)

        deps = bpy.context.evaluated_depsgraph_get()
        terrain_inview_bvh = mathutils.bvhtree.BVHTree.FromObject(terrain_inview, deps)

    def add_fish_school():
        n = random_general(params.get("max_fish_schools", 3))
        for i in range(n):
            selection = density.placement_mask(
                0.1, select_thresh=0, tag=underwater_domain
            )
            fac = creatures.FishSchoolFactory(randint(1e7), bvh=terrain_inview_bvh)
            col = placement.scatter_placeholders_mesh(
                terrain_near,
                fac,
                selection=selection,
                overall_density=1,
                num_placeholders=1,
                altitude=uniform(0.3, 1.5),
            )
            placement.populate_collection(fac, col)

    p.run_stage("fish_school", add_fish_school, default=[])

    def add_handfish_school():
        selection = density.placement_mask(scale=0.05, select_thresh=uniform(0.1, 0.3), tag=underwater_domain)
        fac = creatures.HandfishSchoolFactory(randint(1e7 + 55), bvh=terrain_inview_bvh)
        col = placement.scatter_placeholders_mesh(
            terrain_near,
            fac,
            selection=selection,
            overall_density=1,
            num_placeholders=1,
            altitude=.1
        )
        placement.populate_collection(fac, col)

    p.run_stage('handfish_school', add_handfish_school, default=[])

    def add_rocks(target):
        selection = density.placement_mask(
            scale=0.15,
            select_thresh=0.4,
            normal_thresh=0.7,
            return_scalar=True,
            tag=nonliving_domain,
        )
        _, rock_col = pebbles.apply(target, selection=selection)
        return rock_col

    p.run_stage("rocks", add_rocks, terrain_inview)

    def add_corals(target):
        vertical_faces = density.placement_mask(
            scale=0.15, select_thresh=uniform(0.44, 0.48)
        )
        coral_reef.apply(
            target,
            n=3,
            selection=vertical_faces,
            tag=underwater_domain,
            density=params.get("coral_density", 1.5),
        )
        horizontal_faces = density.placement_mask(
            scale=0.15, normal_thresh=-0.4, normal_thresh_high=0.4
        )
        coral_reef.apply(
            target,
            selection=horizontal_faces,
            n=3,
            horizontal=True,
            tag=underwater_domain,
            density=params.get("horizontal_coral_density", 1.5),
        )

    p.run_stage("corals", add_corals, terrain_inview)

    def add_kelp(terrain_mesh):
        fac = monocot.KelpMonocotFactory(int_hash((scene_seed, 0)), coarse=True)
        selection = density.placement_mask(scale=0.01, tag=underwater_domain, select_thresh=.4)
        placement.scatter_placeholders_mesh(terrain_mesh, fac, altitude=-0.05,
                                            overall_density=params.get('kelp_density', uniform(.05, .2)),
                                            selection=selection, distance_min=5)

    p.run_stage('kelp', add_kelp, terrain_inview)

    p.run_stage('lichen', lambda: lichen.apply(terrain_inview,
                                               selection=density.placement_mask(scale=0.05, select_thresh=.5,
                                                                                normal_thresh=0.0,
                                                                                tag=underwater_domain),
                                               density=random_general(('uniform', 20, 100))))

    def add_coco_images(terrain_inview, classes=[1]):
        for c in classes:
            cocoimageplane.apply(terrain_inview,
                                               scene_seed=int_hash((scene_seed, 0)),
                                               tmp_image_dir=on_the_fly_asset_folder,
                                               category_id=c,
                                               selection=density.placement_mask(scale=0.05, select_thresh=uniform(0.1, 0.3),
                                                                                normal_thresh=0.4,
                                                                                tag=underwater_domain),
                                               density=random_general(('uniform', 2, 4)))
    p.run_stage('cocoimage', add_coco_images, terrain_inview)

    p.run_stage('mollusk', lambda: mollusk.apply(terrain_inview,
                                                 selection=density.placement_mask(scale=0.04, select_thresh=.3,
                                                                                  normal_thresh=0.0,
                                                                                  tag=underwater_domain),
                                                 density=random_general(('uniform', 1, 10))))

    p.run_stage('seaweed', lambda: seaweed.apply(terrain_inview,
                                                 scale=random_general(('clip_gaussian', 0.3, 0.2, 0.1, 0.8)),
                                                 brown_prob=1.0,
                                                 n=20,
                                                 selection=density.placement_mask(scale=0.05, select_thresh=0.3,
                                                                                  normal_thresh=0.4,
                                                                                  tag=underwater_domain)))

    urchin_density = random_general(('uniform', .5, 1))  # no per square metre
    urchin_select_threshold = uniform(0.5, 0.7)  # Lower covers more of the terrain_inview

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

    p.run_stage('scolymia', lambda: scolymia.apply(terrain_inview,
                                                   selection=density.placement_mask(scale=0.05, select_thresh=.5,
                                                                                    tag=underwater_domain)))
    p.run_stage('jellyfish', lambda: jellyfish.apply(terrain_inview,
                                                     selection=density.placement_mask(scale=0.05, select_thresh=.5,
                                                                                      tag=underwater_domain)))

    p.run_stage('colourboard', lambda: place_colourboard(cam.parent, scene_bvh, n=3, alt=0.02, dist_range=(0, 2)))

    def add_plastic_bags(target):
        selection = density.placement_mask(scale=0.1, select_thresh=0.52, normal_thresh=0.7,
                                           tag=nonliving_domain)
        plasticbag.apply(target, selection=selection)

    p.run_stage('plasticbag', add_plastic_bags, terrain_near)

    cube_emitter = weather.spawn_emitter(
        camera_rigs[0], "cube", offset=Vector(), size=30
    )

    butil.constrain_object(
        cube_emitter, "COPY_LOCATION", use_offset=True, target=camera_rigs[0]
    )

    def marine_snow_particles():
        gen = weather.FallingParticles(
            particles.DustMoteFactory(randint(1e7)),
            distribution=weather.particles.marine_snow_param_distribution,
        )
        return gen(cube_emitter)

    p.run_stage("marine_snow_particles", marine_snow_particles)

    p.save_results(output_folder / 'pipeline_coarse.csv')
    return {
        "height_offset": 0,
        "whole_bbox": None,
    }


@gin.configurable
def populate_scene(
    output_folder: Path, scene_seed: int, camera_rigs: list[bpy.types.Object], **params
):
    p = RandomStageExecutor(scene_seed, output_folder, params)

    primary_cams = [rig.children[0] for rig in camera_rigs]

    populated = {}
    # ,
    # meshing_camera=camera, adapt_mesh_method='subdivide', cam_meshing_max_dist=8))
    populated["boulders"] = p.run_stage(
        "populate_boulders",
        use_chance=False,
        default=[],
        fn=lambda: placement.populate_all(
            rocks.BoulderFactory, primary_cams, vis_cull=3
        ),
    )  # ,
    # meshing_camera=camera, adapt_mesh_method='subdivide', cam_meshing_max_dist=8))

    p.run_stage(
        "populate_kelp",
        use_chance=False,
        fn=lambda: placement.populate_all(
            monocot.KelpMonocotFactory, primary_cams, vis_cull=5
        ),
    )

    creature_facs = {
        "crab": creatures.CrabFactory,
        "crustacean": creatures.CrustaceanFactory,
        "fish": creatures.FishFactory,
        "handfish": creatures.HandfishFactory
    }
    for k, fac in creature_facs.items():
        p.run_stage(
            f"populate_{k}",
            use_chance=False,
            fn=lambda: placement.populate_all(fac, cameras=None),
        )

    p.save_results(output_folder / "pipeline_fine.csv")


def main(args):
    scene_seed = init.apply_scene_seed(args.seed)
    mandatory_exclusive = [Path("infinigen_examples/configs_nature/scene_types")]
    init.apply_gin_configs(
        configs=["base_nature.gin"] + args.configs,
        overrides=args.overrides,
        config_folders="infinigen_examples/configs_nature",
        mandatory_folders=mandatory_exclusive,
        mutually_exclusive_folders=mandatory_exclusive,
    )

    execute_tasks.main(
        compose_scene_func=compose_nature,
        populate_scene_func=populate_scene,
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        task=args.task,
        task_uniqname=args.task_uniqname,
        scene_seed=scene_seed,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_folder", type=Path)
    parser.add_argument("--input_folder", type=Path, default=None)
    parser.add_argument(
        "-s", "--seed", default=None, help="The seed used to generate the scene"
    )
    parser.add_argument(
        "-t",
        "--task",
        nargs="+",
        default=["coarse"],
        choices=[
            "coarse",
            "populate",
            "fine_terrain",
            "ground_truth",
            "render",
            "mesh_save",
            "export",
            "renderhidewater",
        ],
    )
    parser.add_argument(
        "-g",
        "--configs",
        nargs="+",
        default=["base"],
        help="Set of config files for gin (separated by spaces) "
        "e.g. --gin_config file1 file2 (exclude .gin from path)",
    )
    parser.add_argument(
        "-p",
        "--overrides",
        nargs="+",
        default=[],
        help="Parameter settings that override config defaults "
        "e.g. --gin_param module_1.a=2 module_2.b=3",
    )
    parser.add_argument("--task_uniqname", type=str, default=None)
    parser.add_argument("-d", "--debug", type=str, nargs="*", default=None)

    args = init.parse_args_blender(parser)

    logging.getLogger("infinigen").setLevel(logging.INFO)
    logging.getLogger("infinigen.core.nodes.node_wrangler").setLevel(logging.CRITICAL)

    if args.debug is not None:
        for name in logging.root.manager.loggerDict:
            if not name.startswith("infinigen"):
                continue
            if len(args.debug) == 0 or any(name.endswith(x) for x in args.debug):
                logging.getLogger(name).setLevel(logging.DEBUG)

    main(args)
