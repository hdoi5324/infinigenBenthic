

### Change Log
Camera Rig
* Downlward looking camera with altitude default of 2m
* HACK: Add first camera at high altitude to force fine resolution of area in animation path. Ignore this camera in rendering.
* Add fixed lights to camera rig

Scene
* change range of ground types in surface registry to just underwater 
* 

3 May
* Camera - set aperture and focus_dist; Use high camera again to get all frames rendered in detail
* generate_auv - tried to add noise.  
* Config - using OcMesher instead of Opaque/TransparentSphericalMesher

4 May
* Render - added noise and lens distortion.  Noise could be improved.
* Animation - used settings for straight camera path

21 May
* Terrain - update surface registry so that 'mountain' uses more surface types.  Mountain used a lot in underwater.
* Assets - adjust selection of where assets are 'scattered' by lowering select_thresh.  
* Assets - added handfish body and arm.
* Assets - added colourboards
* Animation - mow the lawn animation path
* Camera - can use as downward looking with depth of field and aperture OR in ROV with no DOF
* Script for running variations


12 June
* Migrated to infinigen 1.3.3
* Render blender gt - split colours from random_shader into step changes.  Creates 1000 colours.
* Added distortion - set_lens_distortion when configuring cameras in coarse and apply_distortion during render. Based on BlenderProc
* Assets - added plastic bag
* Materials - added 'complexsand' material
* 

### To Do
* handfish - Update nurb body to be more realistic.  More realistic 'hand/arms'. variations in skin. Test schools
* Assets - place assets along camera path
* Assets - add other assets to cause some difficulty eg lichen.  pebbles?

### Issues
* Blender GT - flat shading not saving distinct colours for each instance making bbox generation difficult.
* 
