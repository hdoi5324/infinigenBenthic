"""Camera utility, collection of useful camera functions.

Most of these methods are adopted from BlenderProc including lens distortion and setting
camera parameters.  See https://github.com/DLR-RM/BlenderProc"""

import os
from typing import Union, Optional, List
import gin

import bpy
import numpy as np
from mathutils import Matrix
from scipy.ndimage import map_coordinates


@gin.configurable
def adjust_camera_sensor(cam, sensor_height=18., W=None, H=None):
    scene = bpy.context.scene
    W = scene.render.resolution_x if W is None else W
    H = scene.render.resolution_y if H is None else H
    sensor_width = sensor_height * (W / H)
    # assert sensor_width.is_integer(), (18, W, H)
    cam.data.sensor_height = sensor_height
    cam.data.sensor_width = sensor_width


def set_intrinsics_from_blender_params(cam_ob, lens: float = None, image_width: int = None, image_height: int = None,
                                       clip_start: float = None, clip_end: float = None,
                                       pixel_aspect_x: float = None, pixel_aspect_y: float = None, shift_x: int = None,
                                       shift_y: int = None, lens_unit: str = None):
    """ Sets the camera intrinsics using blenders represenation.

    :param lens: Either the focal length in millimeters or the FOV in radians, depending on the given lens_unit.
    :param image_width: The image width in pixels.
    :param image_height: The image height in pixels.
    :param clip_start: Clipping start.
    :param clip_end: Clipping end.
    :param pixel_aspect_x: The pixel aspect ratio along x.
    :param pixel_aspect_y: The pixel aspect ratio along y.
    :param shift_x: The shift in x direction.
    :param shift_y: The shift in y direction.
    :param lens_unit: Either FOV or MILLIMETERS depending on whether the lens is defined as focal length in
                      millimeters or as FOV in radians.
    """

    # cam_ob = bpy.context.scene.camera
    cam = cam_ob.data

    if lens_unit is not None:
        cam.lens_unit = lens_unit

    if lens is not None:
        # Set focal length
        if cam.lens_unit == 'MILLIMETERS':
            if lens < 1:
                raise Exception("The focal length is smaller than 1mm which is not allowed in blender: " + str(lens))
            cam.lens = lens
        elif cam.lens_unit == "FOV":
            cam.angle = lens
        else:
            raise Exception("No such lens unit: " + lens_unit)

    # Set resolution
    if image_width is not None:
        bpy.context.scene.render.resolution_x = image_width
    if image_height is not None:
        bpy.context.scene.render.resolution_y = image_height

    # Set clipping
    if clip_start is not None:
        cam.clip_start = clip_start
    if clip_end is not None:
        cam.clip_end = clip_end

    # Set aspect ratio
    if pixel_aspect_x is not None:
        bpy.context.scene.render.pixel_aspect_x = pixel_aspect_x
    if pixel_aspect_y is not None:
        bpy.context.scene.render.pixel_aspect_y = pixel_aspect_y

    # Set shift
    if shift_x is not None:
        cam.shift_x = shift_x
    if shift_y is not None:
        cam.shift_y = shift_y


def set_intrinsics_from_K_matrix(cam_ob, K: Union[np.ndarray, Matrix], image_width: int, image_height: int,
                                 clip_start: float = None, clip_end: float = None):
    """ Set the camera intrinsics via a K matrix.

    The K matrix should have the format:
        [[fx, 0, cx],
         [0, fy, cy],
         [0, 0,  1]]

    This method is based on https://blender.stackexchange.com/a/120063.

    :param K: The 3x3 K matrix.
    :param image_width: The image width in pixels.
    :param image_height: The image height in pixels.
    :param clip_start: Clipping start.
    :param clip_end: Clipping end.
    """

    K = Matrix(K)

    # cam = bpy.context.scene.camera.data
    cam = cam_ob.data

    if abs(K[0][1]) > 1e-7:
        raise ValueError(f"Skew is not supported by blender and therefore "
                         f"not by BlenderProc, set this to zero: {K[0][1]} and recalibrate")

    fx, fy = K[0][0], K[1][1]
    cx, cy = K[0][2], K[1][2]

    # If fx!=fy change pixel aspect ratio
    pixel_aspect_x = pixel_aspect_y = 1
    if fx > fy:
        pixel_aspect_y = fx / fy
    elif fx < fy:
        pixel_aspect_x = fy / fx

    # Compute sensor size in mm and view in px
    pixel_aspect_ratio = pixel_aspect_y / pixel_aspect_x
    view_fac_in_px = get_view_fac_in_px(cam, pixel_aspect_x, pixel_aspect_y, image_width, image_height)
    sensor_size_in_mm = get_sensor_size(cam)

    # Convert focal length in px to focal length in mm
    f_in_mm = fx * sensor_size_in_mm / view_fac_in_px

    # Convert principal point in px to blenders internal format
    shift_x = (cx - (image_width - 1) / 2) / -view_fac_in_px
    shift_y = (cy - (image_height - 1) / 2) / view_fac_in_px * pixel_aspect_ratio

    # Finally set all intrinsics
    set_intrinsics_from_blender_params(cam_ob, f_in_mm, image_width, image_height, clip_start, clip_end, pixel_aspect_x,
                                       pixel_aspect_y, shift_x, shift_y, "MILLIMETERS")


def get_sensor_size(cam: bpy.types.Camera) -> float:
    """ Returns the sensor size in millimeters based on the configured sensor_fit.

    :param cam: The camera object.
    :return: The sensor size in millimeters.
    """
    if cam.sensor_fit == 'VERTICAL':
        sensor_size_in_mm = cam.sensor_height
    else:
        sensor_size_in_mm = cam.sensor_width
    return sensor_size_in_mm


def get_view_fac_in_px(cam: bpy.types.Camera, pixel_aspect_x: float, pixel_aspect_y: float,
                       resolution_x_in_px: int, resolution_y_in_px: int) -> int:
    """ Returns the camera view in pixels.

    :param cam: The camera object.
    :param pixel_aspect_x: The pixel aspect ratio along x.
    :param pixel_aspect_y: The pixel aspect ratio along y.
    :param resolution_x_in_px: The image width in pixels.
    :param resolution_y_in_px: The image height in pixels.
    :return: The camera view in pixels.
    """
    # Determine the sensor fit mode to use
    if cam.sensor_fit == 'AUTO':
        if pixel_aspect_x * resolution_x_in_px >= pixel_aspect_y * resolution_y_in_px:
            sensor_fit = 'HORIZONTAL'
        else:
            sensor_fit = 'VERTICAL'
    else:
        sensor_fit = cam.sensor_fit

    # Based on the sensor fit mode, determine the view in pixels
    pixel_aspect_ratio = pixel_aspect_y / pixel_aspect_x
    if sensor_fit == 'HORIZONTAL':
        view_fac_in_px = resolution_x_in_px
    else:
        view_fac_in_px = pixel_aspect_ratio * resolution_y_in_px

    return view_fac_in_px


def set_lens_distortion(cam: bpy.types.Camera, resolution_y, resolution_x,
                        k1: float, k2: float, k3: float = 0.0, p1: float = 0.0, p2: float = 0.0,
                        ) -> np.ndarray:
    """
    this function has been taken from BlenderProc https://github.com/DLR-RM/BlenderProc

    This function applies the lens distortion parameters to obtain an distorted-to-undistorted mapping for all
    natural pixels coordinates of the goal distorted image into the real pixel coordinates of the undistorted
    Blender image. Since such a mapping usually yields void image areas, this function suggests a different
    (usually higher) image resolution for the generated Blender image. Eventually, the function
    `apply_lens_distortion` will make us of this image to fill in the goal distorted image with valid color
    values by interpolation. Note that when adapting the internal image resolution demanded from Blender, the
    camera main point (cx,cy) of the K intrinsic matrix is (internally and temporarily) shifted.

    This function has to be used together with bproc.postprocessing.apply_lens_distortion(), else only the
    resolution is increased but the image(s) will not be distorted.

    :param k1: First radial distortion parameter (of 3rd degree in radial distance) as defined
            by the undistorted-to-distorted Brown-Conrady lens distortion model, which is conform to
            the current DLR CalLab/OpenCV/Bouguet/Kalibr implementations.
            Note that undistorted-to-distorted means that the distortion parameters are multiplied
            by undistorted, normalized camera projections to yield distorted projections, that are in
            turn digitized by the intrinsic camera matrix.
    :param k2: Second radial distortion parameter (of 5th degree in radial distance) as defined
            by the undistorted-to-distorted Brown-Conrady lens distortion model, which is conform
            to the current DLR CalLab/OpenCV/Bouguet/Kalibr implementations.
    :param k3: Third radial distortion parameter (of 7th degree in radial distance) as defined
            by the undistorted-to-distorted Brown-Conrady lens distortion model, which is conform to
            the current DLR CalLab/OpenCV/Bouguet/Kalibr implementations.
            The use of this parameter is discouraged unless the angular field of view is too high,
            rendering it necessary, and the parameter allows for a distorted projection in the whole
            sensor size (which isn't always given by features-driven camera calibration).
    :param p1: First decentering distortion parameter as defined by the undistorted-to-distorted
            Brown-Conrady lens distortion model in (Brown, 1965; Brown, 1971; Weng et al., 1992) and is
            comform to the current DLR CalLab implementation. Note that OpenCV/Bouguet/Kalibr permute them.
            This parameter shares one degree of freedom (j1) with p2; as a consequence, either both
            parameters are given or none. The use of these parameters is discouraged since either current
            cameras do not need them or their potential accuracy gain is negligible w.r.t. image processing.
    :param p2: Second decentering distortion parameter as defined by the undistorted-to-distorted
            Brown-Conrady lens distortion model in (Brown, 1965; Brown, 1971; Weng et al., 1992) and is
            comform to the current DLR CalLab implementation. Note that OpenCV/Bouguet/Kalibr permute them.
            This parameter shares one degree of freedom (j1) with p1; as a consequence, either both
            parameters are given or none. The use of these parameters is discouraged since either current
            cameras do not need them or their potential accuracy gain is negligible w.r.t. image processing.
    :param resolution_x: width in pixels
    :param resolution_y: height in pixels
    :param cam: blender camera object
    :param cx: intrinsics
    :param cy: intrinsics
    :param fx: focal length
    :param fy: focal length
    :return: mapping coordinates from distorted to undistorted image pixels
    """
    if all(v == 0.0 for v in [k1, k2, k3, p1, p2]):
        raise Exception("All given lens distortion parameters (k1, k2, k3, p1, p2) are zero.")

    # save the original image resolution (desired output resolution)
    original_image_resolution = (resolution_y, resolution_x)

    # get the current K matrix (skew==0 in Blender)
    # camera_K_matrix = CameraUtility.get_intrinsics_as_K_matrix()
    camera_K_matrix = get_intrinsics_as_K_matrix(cam, original_image_resolution[1], original_image_resolution[0])
    fx, fy = camera_K_matrix[0][0], camera_K_matrix[1][1]
    cx, cy = camera_K_matrix[0][2], camera_K_matrix[1][2]

    # Get row,column image coordinates for all pixels for row-wise image flattening
    # The center of the upper-left pixel has coordinates [0,0] both in DLR CalDe and python/scipy
    row = np.repeat(np.arange(0, original_image_resolution[0]), original_image_resolution[1])
    column = np.tile(np.arange(0, original_image_resolution[1]), original_image_resolution[0])

    # P_und is the undistorted pinhole projection at z==1 of all image pixels
    P_und = np.linalg.inv(camera_K_matrix) @ np.vstack((column, row, np.ones(np.prod(original_image_resolution[:2]))))

    # P_und are then distorted by the lens, i.e. P_dis = dis(P_und)
    # => Find mapping I_dis(row,column) -> I_und(float,float)
    #
    # We aim at finding the brightness for every discrete pixel of the
    # generated distorted image. In the original undistorted image these
    # are located at real coordinates to be calculated. After that we can
    # interpolate on the original undistorted image.
    # Since dis() cannot be inverted, we iterate (up to ~10 times
    # depending on the AOV and the distortion):
    # 1) assume P_und~=P_dis
    # 2) distort()
    # 3) estimate distance between dist(P_und) and P_dis
    # 4) subtract this distance from the estimated P_und,
    #    perhaps with a factor (>1 for accel, <1 for stability at unstable distortion regions)
    # 5) repeat until P_dis ~ dist(P_und)
    # This works because translations in _dis and _und are approx. equivariant
    # and the mapping is (hopefully) injective (1:1).
    #
    # An alternative, non-iterative approach is P_dis(float,float)=dis(P_und(row,column))
    # and then interpolate on an irregular grid of distorted points. This is faster
    # when generating the mapping matrix but much slower in inference.

    # Init dist at undist
    x = P_und[0, :].copy()
    y = P_und[1, :].copy()
    res = [1e3]
    it = 0
    while res[-1] > 0.15:
        r2 = np.square(x) + np.square(y)
        radial_part = 1 + k1 * r2 + k2 * r2 * r2 + k3 * r2 * r2 * r2
        x_ = x * radial_part + 2 * p2 * x * y + p1 * (r2 + 2 * np.square(x))
        y_ = y * radial_part + 2 * p1 * x * y + p2 * (r2 + 2 * np.square(y))

        error = np.max(np.hypot(fx * (x_ - P_und[0, :]), fy * (y_ - P_und[1, :])))
        res.append(error)
        it += 1

        # Take action if the optimization stalls or gets unstable
        # (distortion models are tricky if badly parameterized, especially in outer regions)
        if (it > 1) and (res[-1] > res[-2] * .99999):
            print("The residual for the worst distorted pixel got unstable/stalled.")
            # factor *= .5
            if it > 1e3:
                raise Exception(
                    "The iterative distortion algorithm is unstable/stalled after 1000 iterations.")
            if error > 1e9:
                print("Some (corner) pixels of the desired image are not defined by the used lens distortion model.")
                print("We invite you to double-check your distortion model.")
                print("The parameters k3,p1,p2 can easily overshoot for regions where the calibration "
                      "software had no datapoints.")
                print("You can either:")
                print("- take more projections (ideally image-filling) at the image corners and repeat calibration,")
                print("- reduce the # of released parameters to calibrate to k1,k2, or")
                print("- reduce the target image size (subtract some lines and columns from the desired resolution")
                print("  and subtract at most that number of lines and columns from the main point location).")
                print("BlenderProc will not generate incomplete images with void regions since these are not "
                      "useful for ML (data leakage).")
                print("For that, you can use the Matlab code in robotic.de/callab, which robustifies against "
                      "these unstable pixels.")
                raise Exception("The iterative distortion algorithm is unstable.")

        # update undistorted projection
        x -= x_ - P_und[0, :]  # * factor
        y -= y_ - P_und[1, :]  # * factor

    # u and v are now the pixel coordinates on the undistorted image that
    # will distort into the row,column coordinates of the distorted image
    u = fx * x + cx
    v = fy * y + cy

    # Stacking this way for the interpolation in the undistorted image array
    mapping_coords = np.vstack([v, u])

    # Find out the image resolution needed from Blender to generate filled-in distorted images of the desired resolution
    min_und_column_needed = np.floor(np.min(u))
    max_und_column_needed = np.ceil(np.max(u))
    min_und_row_needed = np.floor(np.min(v))
    max_und_row_needed = np.ceil(np.max(v))
    columns_needed = max_und_column_needed + 1 - min_und_column_needed
    rows_needed = max_und_row_needed + 1 - min_und_row_needed
    cx_new = cx - min_und_column_needed
    cy_new = cy - min_und_row_needed
    # To avoid spline boundary approximations at the border pixels ('mode' in map_coordinates() )
    columns_needed += 2
    rows_needed += 2
    cx_new += 1
    cy_new += 1
    # suggested resolution for Blender image generation
    new_image_resolution = np.array([columns_needed, rows_needed], dtype=int)

    # Update sensor size using new resolution but keeping same px size.
    pixel_size_in_mm = get_sensor_size(cam.data) / resolution_x
    adjust_camera_sensor(cam, sensor_height=pixel_size_in_mm * columns_needed, W=columns_needed, H=rows_needed)

    # Adapt/shift the mapping function coordinates to the new_image_resolution resolution
    # (if we didn't, the mapping would only be valid for same resolution mapping)
    # (same resolution mapping yields undesired void image areas)
    mapping_coords[0, :] += cy_new - cy
    mapping_coords[1, :] += cx_new - cx

    camera_changed_K_matrix = np.array([[fx, 0, cx],
                                        [0, fy, cy],
                                        [0, 0, 1]])
    # update cx and cy in the K matrix
    camera_changed_K_matrix[0, 2] = cx_new
    camera_changed_K_matrix[1, 2] = cy_new

    # reuse the values, which have been set before
    clip_start = cam.data.clip_start
    clip_end = cam.data.clip_end

    set_intrinsics_from_K_matrix(cam, camera_changed_K_matrix, new_image_resolution[0],
                                 new_image_resolution[1], clip_start, clip_end)

    return mapping_coords


def apply_lens_distortion(image: Union[List[np.ndarray], np.ndarray],
                          mapping_coords: Optional[np.ndarray] = None,
                          orig_res_x: Optional[int] = None,
                          orig_res_y: Optional[int] = None,
                          use_interpolation: bool = True) -> Union[List[np.ndarray], np.ndarray]:
    """
    this function has been taken from BlenderProc https://github.com/DLR-RM/BlenderProc

    This functions applies the lens distortion mapping that needs to be precalculated by
    `bproc.camera.set_lens_distortion()`.

    Without calling this function the `set_lens_distortion` fct. only increases the image resolution and
    changes the K matrix of the camera.

    :param image: a list of images or an image to be distorted
    :param mapping_coords: an array of pixel mappings from undistorted to distorted image
    :param orig_res_x: original and output width resolution of the image
    :param orig_res_y: original and output height resolution of the image
    :param use_interpolation: if this is True, for each pixel an interpolation will be performed, if this is false
                              the nearest pixel will be used
    :return: a list of images or an image that have been distorted, now in the desired (original) resolution
    """

    if mapping_coords is None or orig_res_x is None or orig_res_y is None:
        # if lens distortion was used apply it now
        raise Exception("Applying of a lens distortion is only possible after calling "
                        "bproc.camera.set_lens_distortion(...) and pass 'mapping_coords' and "
                        "'orig_res_x' + 'orig_res_x' to bproc.postprocessing.apply_lens_distortion(...). "
                        "Previously this could also have been done via the CameraInterface module, "
                        "see the example on lens_distortion.")
    interpolation_order = 2 if use_interpolation else 0

    def _internal_apply(input_image: np.ndarray) -> np.ndarray:
        """
        Applies the distortion to the input image
        :param input_image: input image, which will be distorted
        :return: distorted input image
        """
        amount_of_output_channels = 1
        if len(input_image.shape) == 3:
            amount_of_output_channels = input_image.shape[2]
        image_distorted = np.zeros((orig_res_y, orig_res_x, amount_of_output_channels))
        used_dtpye = input_image.dtype
        data = input_image.astype(float)
        # Forward mapping in order to distort the undistorted image coordinates
        # and reshape the arrays into the image shape grid.
        # The reference frame for coords is as in DLR CalDe etc. (the upper-left pixel center is at [0,0])
        mode = 'nearest'
        for i in range(image_distorted.shape[2]):
            if len(input_image.shape) == 3:
                image_distorted[:, :, i] = np.reshape(map_coordinates(data[:, :, i], mapping_coords,
                                                                      order=interpolation_order,
                                                                      mode=mode), image_distorted[:, :, i].shape)
            else:
                image_distorted[:, :, i] = np.reshape(map_coordinates(data, mapping_coords, order=interpolation_order,
                                                                      mode=mode),
                                                      image_distorted[:, :, i].shape)
        # Other options are:
        # - map_coordinates() in all channels at the same time (turns out to be slower)
        # - use torch.nn.functional.grid_sample() instead to do it on the GPU (even in batches)

        if used_dtpye == np.uint8:
            image_distorted = np.clip(image_distorted, 0, 255)
        data = image_distorted.astype(used_dtpye)
        if len(input_image.shape) == 2:
            return data[:, :, 0]
        return data

    if isinstance(image, list):
        return [_internal_apply(img) for img in image]
    if isinstance(image, np.ndarray):
        return _internal_apply(image)
    raise Exception(f"This type can not be worked with here: {type(image)}, only "
                    f"np.ndarray or list of np.ndarray are supported")


def get_intrinsics_as_K_matrix(cam_ob, resolution_x_in_px, resolution_y_in_px) -> np.ndarray:
    """ Returns the current set intrinsics in the form of a K matrix.

    This is basically the inverse of the the set_intrinsics_from_K_matrix() function.

    :return: The 3x3 K matrix
    """
    cam = cam_ob.data

    f_in_mm = cam.lens
    # resolution_x_in_px = bpy.context.scene.render.resolution_x
    # resolution_y_in_px = bpy.context.scene.render.resolution_y

    # Compute sensor size in mm and view in px
    pixel_aspect_ratio = bpy.context.scene.render.pixel_aspect_y / bpy.context.scene.render.pixel_aspect_x
    view_fac_in_px = get_view_fac_in_px(cam, bpy.context.scene.render.pixel_aspect_x,
                                        bpy.context.scene.render.pixel_aspect_y, resolution_x_in_px, resolution_y_in_px)
    sensor_size_in_mm = get_sensor_size(cam)

    # Convert focal length in mm to focal length in px
    fx = f_in_mm / sensor_size_in_mm * view_fac_in_px
    fy = fx / pixel_aspect_ratio

    # Convert principal point in blenders format to px
    cx = (resolution_x_in_px - 1) / 2 - cam.shift_x * view_fac_in_px
    cy = (resolution_y_in_px - 1) / 2 + cam.shift_y * view_fac_in_px / pixel_aspect_ratio

    # Build K matrix
    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0, 0, 1]])
    return K


def save_distortion_parameters(cam_ob, mapping_coords, original_resolution, parameter_dir="./"):
    cam_name_string = cam_ob.name.replace("/", "_")
    np.save(os.path.join(parameter_dir, f"{cam_name_string}_mapping_coords.npy"), mapping_coords)
    np.save(os.path.join(parameter_dir, f"{cam_name_string}_orig_res.npy"), original_resolution)
    return True


def load_distortion_parameters(cam_ob, parameter_dir="./"):
    cam_name_string = cam_ob.name.replace("/", "_")
    mapping_coords = np.load(os.path.join(parameter_dir, f"{cam_name_string}_mapping_coords.npy"))
    original_resolution = np.load(os.path.join(parameter_dir, f"{cam_name_string}_orig_res.npy"))
    return mapping_coords, original_resolution


def remove_segmap_noise(image: Union[list, np.ndarray], image_bit=0, threshold=200) -> Union[list, np.ndarray]:
    """
    A function that takes an image and a few 2D indices, where these indices correspond to pixel values in
    segmentation maps, where these values are not real labels, but some deviations from the real labels, that were
    generated as a result of Blender doing some interpolation, smoothing, or other numerical operations.

    Assumes that noise pixel values won't occur more than 100 times.

    :param image: ndarray of the .exr segmap
    :return: The denoised segmap image
    """

    if isinstance(image, list) or hasattr(image, "shape") and len(image.shape) > 3:
        return [remove_segmap_noise(img) for img in image]

    noise_indices = determine_noisy_pixels(image, image_bit=image_bit, threshold=threshold)

    for index in noise_indices:
        neighbors = get_pixel_neighbors(image, index[0], index[
            1])  # Extracting the indices surrounding 3x3 neighbors
        curr_val = image[index[0]][index[1]][0]  # Current value of the noisy pixel

        neighbor_vals = [image[neighbor[0]][neighbor[1]] for neighbor in
                         neighbors]  # Getting the values of the neighbors
        # Getting the unique values only
        neighbor_vals = np.unique(np.array([np.array(index) for index in neighbor_vals]))

        min_val = 10000000000
        min_idx = 0

        # Here we iterate through the unique values of the neighbor and find the one closest to the current noisy value
        for idx, n in enumerate(neighbor_vals):
            # Is this closer than the current closest value?
            if n - curr_val <= min_val:
                # If so, update
                min_val = n - curr_val
                min_idx = idx

        # Now that we have found the closest value, assign it to the noisy value
        new_val = neighbor_vals[min_idx]
        image[index[0]][index[1]] = np.array([new_val, new_val, new_val])

    return image


def get_pixel_neighbors(data: np.ndarray, i: int, j: int) -> np.ndarray:
    """ Returns the valid neighbor pixel indices of the given pixel.

    :param data: The whole image data.
    :param i: The row index of the pixel
    :param j: The col index of the pixel.
    :return: A list of neighbor point indices.
    """
    neighbors = []
    for p in range(max(0, i - 1), min(data.shape[0], i + 2)):
        for q in range(max(0, j - 1), min(data.shape[1], j + 2)):
            if not (p == i and q == j):  # We don't want the current pixel, just the neighbors
                neighbors.append([p, q])

    return np.array(neighbors)


def determine_noisy_pixels(image: np.ndarray, threshold=100, image_bit=16) -> np.ndarray:
    """
    :param image: The image data.
    :return: a list of 2D indices that correspond to the noisy pixels. One criterion of finding \
                          these pixels is to use a histogram and find the pixels with frequencies lower than \
                          a threshold, e.g. 100.
    """
    # The map was scaled to be ranging along the entire 16-bit color depth, and this is the scaling down operation
    # that should remove some noise or deviations
    image = (image * 37) / (np.power(2, image_bit))  # assuming 16 bit color depth
    image = image.astype(np.int32)
    b, counts = np.unique(image.flatten(), return_counts=True)

    # Removing further noise where there are some stray pixel values with very small counts, by assigning them to
    # their closest (numerically, since this deviation is a
    # result of some numerical operation) neighbor.
    hist = sorted((np.asarray((b, counts)).T), key=lambda x: x[1])
    # Assuming the stray pixels wouldn't have a count of more than 100
    noise_vals = [h[0] for h in hist if h[1] <= threshold]
    noise_indices = np.argwhere(is_in(image, noise_vals))

    return noise_indices


def is_in(element, test_elements, assume_unique=False, invert=False):
    """ As np.isin is only available after v1.13 and blender is using 1.10.1 we have to implement it manually. """
    element = np.asarray(element)
    return np.in1d(element, test_elements, assume_unique=assume_unique, invert=invert).reshape(element.shape)
