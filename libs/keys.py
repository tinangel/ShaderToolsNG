# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>
import bpy

#Materials keys
def MaterialsKeys():
    temp = \
        (
         "menu_category_car_paint", "menu_category_dirt", "menu_category_fabric_clothes", "menu_category_fibre_fur",
         "menu_category_fancy","menu_category_glass", "menu_category_halo", "menu_category_liquids", "menu_category_metal", 
         "menu_category_misc", "menu_category_nature", "menu_category_organic", "menu_category_personal", "menu_category_plastic", 
         "menu_category_sky", "menu_category_space", "menu_category_stone", "menu_category_toon", "menu_category_wall", 
         "menu_category_water", "menu_category_wood",
         )
    return temp
#end Materials keys
#Options keys
def OptionsKeys():
    temp = \
        (
         "menu_configuration_option_delete", "menu_configuration_option_save", 
         #"menu_configuration_option_copy", "menu_configuration_option_update",
         )
    return temp
#end Options keys
#Api keys
def ApiKeys():
    temp = \
        (      
         "context_object","context_material","context_texture","context_scene","context_render","type","preview_render_type","type",
         "diffuse_color","diffuse_shader","diffuse_intensity","use_diffuse_ramp","roughness","diffuse_fresnel","diffuse_fresnel_factor","darkness","diffuse_toon_size",
         "diffuse_toon_smooth","specular_color","specular_shader","specular_intensity","use_specular_ramp","specular_hardness","specular_ior",
         "specular_toon_size","specular_toon_smooth","specular_slope","emit","ambient","translucency","use_shadeless","use_tangent_shading","use_cubic",
         "use_transparency","transparency_method","alpha","specular_alpha","raytrace_transparency_fresnel","raytrace_transparency_fresnel_factor",
         "raytrace_transparency_ior","raytrace_transparency_filter","raytrace_transparency_falloff","raytrace_transparency_depth_max","raytrace_transparency_depth",
         "raytrace_transparency_gloss_factor","raytrace_transparency_gloss_threshold","raytrace_transparency_gloss_samples","raytrace_mirror_use",
         "raytrace_mirror_reflect_factor","raytrace_mirror_fresnel","mirror_color","raytrace_mirror_fresnel_factor","raytrace_mirror_depth",
         "raytrace_mirror_distance","raytrace_mirror_fade_to","raytrace_mirror_gloss_factor","raytrace_mirror_gloss_threshold","raytrace_mirror_gloss_samples",
         "raytrace_mirror_gloss_anisotropic","subsurface_scattering_use","subsurface_scattering_ior","subsurface_scattering_scale","subsurface_scattering_color",
         "subsurface_scattering_color_factor","subsurface_scattering_texture_factor","subsurface_scattering_radius","subsurface_scattering_front",
         "subsurface_scattering_back","subsurface_scattering_error_threshold","strand_root_size","strand_tip_size","strand_size_min","strand_width_fade",
         "strand_uv_layer","strand_use_blender_units","strand_use_tangent_shading","strand_shape","strand_blend_distance","use_raytrace","use_full_oversampling",
         "use_sky","use_mist","invert_z","use_face_texture","use_face_texture_alpha","use_vertex_color_paint","use_vertex_color_light","use_object_color","offset_z",
         "pass_index","light_group","use_light_group_exclusive","use_shadows","use_transparent_shadows","use_cast_shadows_only","shadow_cast_alpha",
         "use_only_shadow","volume_density","volume_density_scale","volume_scattering","volume_asymmetry","volume_emission","volume_emission_color",
         "volume_reflection","volume_reflection_color","volume_transmission_color","volume_light_method","volume_use_external_shadows","volume_use_light_cache",
         "volume_cache_resolution","volume_ms_diffusion","volume_ms_spread","volume_ms_intensity","volume_step_method","volume_step_size","volume_depth_threshold",
         "halo_size","halo_hardness","halo_seed","halo_add","halo_use_texture","halo_use_vertex_normal","halo_use_extreme_alpha","halo_use_shaded","halo_use_soft",
         "halo_use_ring","halo_ring_count","halo_use_lines","halo_line_count","halo_use_star","halo_star_tip_count","halo_use_flare_mode","halo_flare_size",
         "halo_flare_boost","halo_flare_seed","halo_flare_subflare_count","halo_flare_subflare_size","use_textures","texture_noise_basis_2",
         "texture_wood_type","texture_noise_type","texture_noise_basis","texture_noise_scale","texture_nabla","texture_turbulence","texture_distance_metric",
         "texture_minkovsky_exponent","texture_color_mode","texture_noise_intensity","texture_weight_1","texture_weight_2","texture_weight_3","texture_weight_4",
         "texture_stucci_type","texture_musgrave_type","texture_dimension_max","texture_lacunarity","texture_octaves","texture_offset","texture_gain",
         "texture_marble_type","texture_noise_depth","texture_cloud_type","texture_progression","texture_voxel_data_file_format","texture_image","texture_image_name",
         "texture_image_source","texture_image_filepath","texture_image_filepath_raw","texture_image_file_format","texture_image_user_frame_duration",
         "texture_image_user_frame_start","texture_image_user_frame_offset","texture_image_user_fields_per_frame","texture_image_user_use_auto_refresh",
         "texture_image_user_use_cyclic","texture_voxel_data_interpolation","texture_voxel_data_extension","texture_voxel_data_intensity","texture_voxel_data_filepath",
         "texture_voxel_data_resolution","texture_voxel_data_use_still_frame","texture_voxel_data_still_frame","texture_voxel_data_domain_object",
         "texture_voxel_data_domain_object_name","texture_voxel_data_smoke_data_type","texture_point_density_point_source","texture_point_density_object",
         "texture_point_density_object_name","texture_point_density_radius","texture_point_density_particle_system","texture_point_density_falloff",
         "texture_point_density_falloff_speed_scale","texture_point_density_particle_cache_space","texture_point_density_use_falloff_curve",
         "texture_point_density_color_source","texture_point_density_speed_scale","texture_point_density_use_turbulence","texture_point_density_turbulence_influence",
         "texture_point_density_turbulence_scale","texture_point_density_turbulence_depth","texture_point_density_turbulence_strength","texture_image_use_fields",
         "texture_image_use_premultiply","texture_image_field_order","texture_image_generated_width","texture_image_generated_height","texture_image_generated_type",
         "texture_image_use_generated_float","texture_use_alpha","texture_use_calculate_alpha","texture_invert_alpha","texture_use_flip_axis","texture_use_normal_map",
         "normal_map_space","texture_use_derivative_map","texture_use_mipmap","texture_use_mipmap_gauss","texture_use_interpolation","texture_filter_type",
         "texture_filter_eccentricity","texture_filter_size","texture_use_filter_size_min","texture_filter_probes","texture_extension","texture_repeat_x",
         "texture_repeat_y","texture_use_mirror_x","texture_use_mirror_y","texture_crop_min_x","texture_crop_min_y","texture_crop_max_x","texture_crop_max_y",
         "texture_use_checker_even","texture_use_checker_odd","texture_checker_distance","texture_noise_distortion","texture_distortion",
         "texture_environment_map_source","texture_environment_map_mapping","texture_environment_map_viewpoint_object",
         "texture_environment_map_viewpoint_object_name","texture_environment_map_layers_ignore","texture_environment_map_resolution",
         "texture_environment_map_depth","texture_environment_map_clip_start","texture_environment_map_clip_end","texture_coords","object","uv_layer",
         "use_from_dupli","use_from_original","mapping","mapping_x","mapping_y","mapping_z","offset","scale","texture_use_color_ramp",
         "texture_factor_red","texture_factor_green","texture_factor_blue","texture_intensity","texture_contrast","texture_saturation","use_map_diffuse",
         "use_map_color_diffuse","use_map_alpha","use_map_translucency","use_map_ambient","use_map_emit","use_map_mirror","use_map_raymir","use_map_specular",
         "use_map_color_spec","use_map_hardness","use_map_normal","use_map_warp","use_map_displacement","diffuse_factor","diffuse_color_factor","alpha_factor",
         "translucency_factor","specular_factor","specular_color_factor","hardness_factor","ambient_factor","emit_factor","mirror_factor","raymir_factor",
         "normal_factor","warp_factor","displacement_factor","blend_type","use_rgb_to_intensity","color","invert","use_stencil","default_value","bump_method",
         "bump_objectspace", "diffuse_ramp_blend","diffuse_ramp_input","diffuse_ramp_factor","diffuse_ramp_interpolation",
         "diffuse_ramp_elements_position","diffuse_ramp_elements_color","specular_ramp_blend","specular_ramp_input","specular_ramp_factor",
         "specular_ramp_interpolation","specular_ramp_elements_position","specular_ramp_elements_color","texture_color_ramp_interpolation",
         "texture_color_ramp_elements_position","texture_color_ramp_elements_color","texture_point_density_color_ramp_interpolation",
         "texture_point_density_color_ramp_elements_position","texture_point_density_color_ramp_elements_color", "render_resolution_x",
         "render_resolution_y","render_resolution_percentage","render_pixel_aspect_x","render_pixel_aspect_y","render_use_antialiasing",
         "render_antialiasing_samples","render_use_full_sample","render_filepath","render_file_format","render_color_mode","render_use_file_extension",
         "render_use_overwrite","render_use_placeholder","render_file_quality", "utils_script_paths", "utils_resource_path", "app_version", "data_filepath", 
         "props", "utils_unregister_class", "utils_register_class", "ops", "ops_object", "types_panel", "types_operator", "invoke_props_dialog", "app_binary_path",
         "invoke_search_popup", "active_material", "fileselect_add", "materials_new", "shadow_only_type", "use_cast_shadows_only", "use_cast_buffer_shadows", "shadow_buffer_bias",
         "use_ray_shadow_bias", "shadow_ray_bias", "use_cast_approximate", "material_slot_add", "material_slots", "diffuse_ramp_elements", "specular_ramp_elements", 
         "texture_color_ramp_elements", "texture_point_density_color_ramp_elements", "texture_slots_values", "texture_slots_items","texture_slots", "texture_slots_create",
         "texture_slots_values_use", "texture_slots_values_texture_type", "texture_use_preview_alpha", "texture_slots_texture_name", "texture_slots_new", "texture_slots_texture_type",
         "texture_slots_add", "texture_image_save_render", "texture_image_save_as", "texture_image_pack", "texture_image_unpack", "texture_image_load", "material_name", "render_render")
    return temp
#end Api keys
#Langages keys
def LangagesKeys():
    temp = \
        [      
         "num_languages", "keyboard", "name_language", "panel_name", "buttons_open", "buttons_save", "buttons_config", "buttons_export", "buttons_import", "buttons_informations", 
         "buttons_help", "buttons_credits", "buttons_create", "menu_bookmarks_name", "menu_information_title", "menu_information_name_title", "menu_information_name_default",
         "menu_information_creator_title", "menu_information_creator_default", "menu_information_category_title", "menu_information_category_default", "menu_information_description_title",
         "menu_information_description_default", "menu_information_link_title", "menu_information_link_default", "menu_information_email_title", "menu_information_email_default",
         "menu_help_title", "bl_id_name_open","bl_id_name_save", "bl_id_name_export", "bl_id_name_import", "bl_id_name_create", "bl_id_name_help", "bl_id_name_credits", "bl_id_name_config", "space_access_name",
         "menu_configuration_select_title", "menu_configuration_name", "menu_configuration_options", "menu_configuration_informations", "menu_configuration_material_name",
         "menu_configuration_description", "menu_configuration_creator_name", "menu_configuration_web_link", "menu_configuration_email", "menu_configuration_category", 
         "menu_configuration_preview_parameters", "menu_configuration_resolution_x", "menu_configuration_resolution_y", "menu_configuration_base_parameters", "menu_configuration_base_path",
         "menu_configuration_option_save", "menu_configuration_option_delete", "menu_configuration_option_update", "menu_configuration_option_copy", "menu_configuration_key_words", 
         "menu_category_car_paint", "menu_category_dirt", "menu_category_fabric_clothes", "menu_category_fancy", "menu_category_fibre_fur", "menu_category_glass", "menu_category_halo", 
         "menu_category_liquids", "menu_category_metal", "menu_category_misc", "menu_category_nature", "menu_category_organic", "menu_category_personal", "menu_category_plastic", "menu_category_sky",
         "menu_category_space", "menu_category_stone", "menu_category_toon", "menu_category_wall", "menu_category_water", "menu_category_wood", "buttons_update_blender",
         "menu_configuration_default_config", "bl_id_config_search", "menu_configuration_langage_choice", "menu_configuration_current_index", "take_preview", "buttons_log",
         "menu_import_label001", "menu_import_label002",
         ]
    for i in range(1, 31):
        temp.append("menu_error_error%03d" % i)
    return temp
#end Langages keys
#Configurations keys
def ConfigurationsKeys():
    temp = \
        (      
         "num_configuration", "default_config", "name", "database_path", "author", "description", "web_link", "material_name", "category", "email_creator",
         "resolution_min", "resolution_max", "language", "error_folder", "html_folder", "pack_folder", "temp_folder", "zip_folder", "workbase_file_path",
         "help_file_path", "img_file_path", "bin_folder", "key_words", "option", "resolution_default_x", "resolution_default_y", "take_preview", 
         )
    return temp
#end Configurations keys
#About keys
def AboutKeys():
    temp = \
        (      
         "num_about", "name", "function", "web", "email", "other",
         )
    return temp
#end About keys
#Credits keys
def CreditsKeys():
    temp = \
        (
         "author", "community", "translate", "developer",
         "testing_corrections", "comments_suggestions",   
         )
    return temp
#end Credits keys
#Test keys
def TestKeys():
    temp = \
        (
         "num_test", "text", "float", "bool", "blob", "date", "time",
         )
    return temp
#end Test keys
#Material Properties keys
def MaterialsPropertiesKeys(api_functions):
    mat_properties  = \
    {"diffuse_color":(api_functions['diffuse_color'], ''),"diffuse_shader":(api_functions['diffuse_shader'], 'yes'),
    "diffuse_intensity":(api_functions['diffuse_intensity'], ''),"roughness":(api_functions['roughness'], ''),
    "diffuse_toon_size":(api_functions['diffuse_toon_size'], ''),"diffuse_toon_smooth":(api_functions['diffuse_toon_smooth'], ''),
    "diffuse_toon_size":(api_functions['diffuse_toon_size'], ''),"darkness":(api_functions['darkness'], ''),
    "diffuse_fresnel":(api_functions['diffuse_fresnel'], ''),"diffuse_fresnel_factor":(api_functions['roughness'], ''),
    "specular_shader":(api_functions['specular_shader'], 'yes'),"specular_color":(api_functions['specular_color'], ''),
    "specular_intensity":(api_functions['specular_intensity'], ''),"specular_hardness":(api_functions['specular_hardness'], ''),
    "specular_ior":(api_functions['specular_ior'], ''),"specular_toon_size":(api_functions['roughness'], ''),
    "specular_toon_smooth":(api_functions['roughness'], ''),"emit":(api_functions['emit'], ''),"ambient":(api_functions['ambient'], ''),
    "translucency":(api_functions['translucency'], ''),"use_shadeless":(api_functions['use_shadeless'], ''),
    "use_tangent_shading":(api_functions['use_tangent_shading'], ''),"use_transparency":(api_functions['use_transparency'], ''),                        
    "transparency_method":(api_functions['transparency_method'], 'yes'),"alpha":(api_functions['alpha'], ''),
    "raytrace_transparency.fresnel":(api_functions['raytrace_transparency_fresnel'], ''),
    "specular_alpha":(api_functions['specular_alpha'], ''),"light_group":(api_functions['light_group'], ''),
    "raytrace_transparency.fresnel_factor":(api_functions['raytrace_transparency_fresnel_factor'], ''),
    "raytrace_transparency.ior":(api_functions['raytrace_transparency_ior'], ''),
    "raytrace_transparency.filter":(api_functions['raytrace_transparency_filter'], ''),                        
    "raytrace_transparency.falloff":(api_functions['raytrace_transparency_falloff'], ''),
    "raytrace_transparency.depth_max":(api_functions['raytrace_transparency_depth_max'], ''),
    "raytrace_transparency.depth":(api_functions['raytrace_transparency_depth'], ''),
    "raytrace_transparency.gloss_factor":(api_functions['raytrace_transparency_gloss_factor'], ''),
    "raytrace_transparency.gloss_threshold":(api_functions['raytrace_transparency_gloss_threshold'], ''),
    "raytrace_transparency.gloss_samples":(api_functions['raytrace_transparency_gloss_samples'], ''),
    "raytrace_mirror.use":(api_functions['raytrace_mirror_use'], ''),"use_light_group_exclusive":(api_functions['light_group'], ''),
    "raytrace_mirror.reflect_factor":(api_functions['raytrace_mirror_reflect_factor'], ''),                        
    "raytrace_mirror.fresnel":(api_functions['raytrace_mirror_fresnel'], ''),
    "mirror_color":(api_functions['mirror_color'], ''),"raytrace_mirror.fresnel_factor":(api_functions['raytrace_mirror_fresnel_factor'], ''),
    "raytrace_mirror.depth":(api_functions['raytrace_mirror_depth'], ''),"raytrace_mirror.distance":(api_functions['raytrace_mirror_distance'], ''),
    "raytrace_mirror.fade_to":(api_functions['raytrace_mirror_fade_to'], 'yes'),"raytrace_mirror.gloss_factor":(api_functions['raytrace_mirror_gloss_factor'], ''),
    "raytrace_mirror.gloss_threshold":(api_functions['raytrace_mirror_gloss_threshold'], ''),                        
    "raytrace_mirror.gloss_samples":(api_functions['raytrace_mirror_gloss_samples'], ''),"strand.uv_layer":(api_functions['strand_uv_layer'], ''),
    "raytrace_mirror.gloss_anisotropic":(api_functions['raytrace_mirror_gloss_anisotropic'], ''),
    "subsurface_scattering.use":(api_functions['subsurface_scattering_use'], ''),
    "subsurface_scattering.ior":(api_functions['subsurface_scattering_ior'], ''),
    "subsurface_scattering.scale":(api_functions['subsurface_scattering_scale'], ''),
    "subsurface_scattering.color":(api_functions['subsurface_scattering_color'], ''),
    "subsurface_scattering.color_factor":(api_functions['subsurface_scattering_color_factor'], ''),
    "subsurface_scattering.texture_factor":(api_functions['subsurface_scattering_texture_factor'], ''),                        
    "subsurface_scattering.radius":(api_functions['subsurface_scattering_radius'], ''),
    "subsurface_scattering.front":(api_functions['subsurface_scattering_front'], ''),
    "subsurface_scattering.back":(api_functions['subsurface_scattering_back'], ''),
    "subsurface_scattering.error_threshold":(api_functions['subsurface_scattering_error_threshold'], ''),
    "strand.root_size":(api_functions['strand_root_size'], ''),"strand.tip_size":(api_functions['strand_tip_size'], ''),
    "strand.size_min":(api_functions['strand_size_min'], ''),"strand.use_blender_units":(api_functions['strand_use_blender_units'], ''),                        
    "strand.use_tangent_shading":(api_functions['strand_use_tangent_shading'], ''),"strand.shape":(api_functions['strand_shape'], ''),
    "strand.width_fade":(api_functions['strand_width_fade'], ''),"strand.blend_distance":(api_functions['strand_blend_distance'], ''),
    "use_raytrace":(api_functions['use_raytrace'], ''),"use_full_oversampling":(api_functions['use_full_oversampling'], ''),
    "use_sky":(api_functions['use_sky'], ''),"use_mist":(api_functions['use_mist'], ''),"invert_z":(api_functions['invert_z'], ''),
    "offset_z":(api_functions['offset_z'], ''),"use_face_texture":(api_functions['use_face_texture'], ''),
    "use_face_texture_alpha":(api_functions['use_face_texture_alpha'], ''),"use_vertex_color_paint":(api_functions['use_vertex_color_paint'], ''),
    "use_vertex_color_light":(api_functions['use_vertex_color_light'], ''),"use_object_color":(api_functions['use_object_color'], ''),
    "pass_index":(api_functions['pass_index'], ''),"use_shadows":(api_functions['use_shadows'], ''),
    "use_transparent_shadows":(api_functions['use_transparent_shadows'], ''),"use_cast_shadows_only":(api_functions['use_cast_shadows_only'], ''),
    "shadow_cast_alpha":(api_functions['shadow_cast_alpha'], ''),"use_only_shadow":(api_functions['use_only_shadow'], ''),
    "shadow_only_type":(api_functions['shadow_only_type'], 'yes'),"use_cast_buffer_shadows":(api_functions['use_cast_buffer_shadows'], ''),
    "shadow_buffer_bias":(api_functions['shadow_buffer_bias'], ''),"use_ray_shadow_bias":(api_functions['use_ray_shadow_bias'], ''),
    "shadow_ray_bias":(api_functions['shadow_ray_bias'], ''),"use_cast_approximate":(api_functions['use_cast_approximate'], ''),
    "volume.density":(api_functions['volume_density'], ''),"volume.density_scale":(api_functions['volume_density_scale'], ''),
    "volume.scattering":(api_functions['volume_scattering'], ''),"volume.asymmetry":(api_functions['volume_asymmetry'], ''),
    "volume.emission":(api_functions['volume_emission'], ''),"volume.emission_color":(api_functions['volume_emission_color'], ''),
    "volume.reflection":(api_functions['volume_reflection'], ''),"volume.reflection_color":(api_functions['volume_reflection_color'], ''),
    "volume.transmission_color":(api_functions['volume_transmission_color'], ''),"volume.light_method":(api_functions['volume_light_method'], 'yes'),
    "volume.use_external_shadows":(api_functions['volume_use_external_shadows'], ''),"volume.use_light_cache":(api_functions['volume_use_light_cache'], ''),
    "volume.cache_resolution":(api_functions['volume_cache_resolution'], ''),"volume.ms_diffusion":(api_functions['volume_ms_diffusion'], ''),
    "volume.ms_spread":(api_functions['volume_ms_spread'], ''),"volume.ms_intensity":(api_functions['volume_ms_intensity'], ''),
    "volume.step_method":(api_functions['volume_step_method'], 'yes'),"volume.step_size":(api_functions['volume_step_size'], ''),
    "volume.depth_threshold":(api_functions['volume_depth_threshold'], ''),"halo.size":(api_functions['halo_size'], ''),
    "halo.hardness":(api_functions['halo_hardness'], ''),"halo.seed":(api_functions['halo_seed'], ''),"halo.add":(api_functions['halo_add'], ''),
    "halo.use_texture":(api_functions['halo_use_texture'], ''),"halo.use_vertex_normal":(api_functions['halo_use_vertex_normal'], ''),
    "halo.use_extreme_alpha":(api_functions['halo_use_extreme_alpha'], ''),"halo.use_shaded":(api_functions['halo_use_shaded'], ''),
    "halo.use_soft":(api_functions['halo_use_soft'], ''),"halo.use_ring":(api_functions['halo_use_ring'], ''),
    "halo.ring_count":(api_functions['halo_ring_count'], ''),"halo.use_lines":(api_functions['halo_use_lines'], ''),
    "halo.line_count":(api_functions['halo_line_count'], ''),"halo.use_star":(api_functions['halo_use_star'], ''),
    "halo.star_tip_count":(api_functions['halo_star_tip_count'], ''),"halo.use_flare_mode":(api_functions['halo_use_flare_mode'], ''),
    "halo.flare_size":(api_functions['halo_flare_size'], ''),"halo.flare_boost":(api_functions['halo_flare_boost'], ''),
    "halo.flare_seed":(api_functions['halo_flare_seed'], ''),"halo.flare_subflare_count":(api_functions['halo_flare_subflare_count'], ''),
    "halo.flare_subflare_size":(api_functions['halo_flare_subflare_size'], ''),}
    return mat_properties
#end Material Properties keys
#Formats Supported Properties keys
def ImageFileFormatKeys(format):
    format_supported =  {"BMP":'.bmp', "PNG":'.png', "JPEG":'.jpg', "TARGA":'.tga', "TARGA_RAW":'.tga',}
    if format == '': return format_supported
    else: return format_supported[format]
#end Formats Supported Properties keys
#Ramps Properties keys
def RampsPropertiesKeys(api_functions):
    ramps_properties  = \
    {"diffuse_ramp.blend":(api_functions['diffuse_ramp_blend'], ''),"diffuse_ramp.input":(api_functions['diffuse_ramp_input'], ''),
    "diffuse_ramp.factor":(api_functions['diffuse_ramp_factor'], ''),"diffuse_ramp.interpolation":(api_functions['diffuse_ramp_interpolation'], 'yes'),
    "diffuse_ramp.elements.position":(api_functions['diffuse_ramp_elements_position'], ''),"diffuse_ramp.elements.color":(api_functions['diffuse_ramp_elements_color'], ''),
    "diffuse_ramp.elements":(api_functions['diffuse_ramp_elements'], ''),
    "specular_ramp.blend":(api_functions['specular_ramp_blend'], ''),"specular_ramp.input":(api_functions['specular_ramp_input'], ''),
    "specular_ramp.factor":(api_functions['specular_ramp_factor'], ''),"specular_ramp.interpolation":(api_functions['specular_ramp_interpolation'], 'yes'),
    "specular_ramp.elements.position":(api_functions['specular_ramp_elements_position'], ''),"specular_ramp.elements.color":(api_functions['specular_ramp_elements_color'], ''),
    "specular_ramp.elements":(api_functions['specular_ramp_elements'], ''),
    "color_ramp.interpolation":(api_functions['texture_color_ramp_interpolation'], 'yes'),
    "color_ramp.elements.position":(api_functions['texture_color_ramp_elements_position'], ''),"color_ramp.elements.color":(api_functions['texture_color_ramp_elements_color'], ''),
    "color_ramp.elements":(api_functions['texture_color_ramp_elements'], ''),
    "point_density_color_ramp.interpolation":(api_functions['texture_point_density_color_ramp_interpolation'], 'yes'),
    "point_density_color_ramp.elements.position":(api_functions['texture_point_density_color_ramp_elements_position'], ''),
    "point_density_color_ramp.elements.color":(api_functions['texture_point_density_color_ramp_elements_color'], ''), 
    "point_density_color_ramp.elements":(api_functions['texture_point_density_color_ramp_elements'], ''),}
    return ramps_properties
#end Material Properties keys
#SurfaceWire keys
def SurfaceWireKeys():
    surface_wire  = \
    ("diffuse_color","diffuse_shader","diffuse_intensity","roughness","diffuse_toon_size","diffuse_toon_smooth",
    "diffuse_toon_size","darkness","diffuse_fresnel","diffuse_fresnel_factor","specular_shader","specular_color",
    "specular_intensity","specular_hardness","specular_ior","specular_toon_size","specular_toon_smooth","emit",
    "ambient","translucency","use_shadeless","use_tangent_shading","use_transparency","transparency_method",
    "alpha","raytrace_transparency.fresnel","specular_alpha","raytrace_transparency.fresnel_factor",
    "raytrace_transparency.ior","raytrace_transparency.filter","raytrace_transparency.falloff",
    "raytrace_transparency.depth_max","raytrace_transparency.depth","raytrace_transparency.gloss_factor",
    "raytrace_transparency.gloss_threshold","raytrace_transparency.gloss_samples","raytrace_mirror.use",
    "raytrace_mirror.reflect_factor","raytrace_mirror.fresnel","mirror_color","raytrace_mirror.fresnel_factor",
    "raytrace_mirror.depth","raytrace_mirror.distance","raytrace_mirror.fade_to","raytrace_mirror.gloss_factor",
    "raytrace_mirror.gloss_threshold","raytrace_mirror.gloss_samples","raytrace_mirror.gloss_anisotropic",
    "subsurface_scattering.use","subsurface_scattering.ior","subsurface_scattering.scale",
    "subsurface_scattering.color","subsurface_scattering.color_factor","subsurface_scattering.texture_factor",                        
    "subsurface_scattering.radius","subsurface_scattering.front","subsurface_scattering.back",
    "subsurface_scattering.error_threshold","strand.root_size","strand.tip_size","strand.size_min","strand.use_blender_units",                        
    "strand.use_tangent_shading","strand.shape","strand.width_fade","strand.blend_distance","use_raytrace","use_full_oversampling",
    "use_sky","use_mist","invert_z","offset_z","use_face_texture","use_face_texture_alpha","use_vertex_color_paint",
    "use_vertex_color_light","use_object_color","pass_index","use_shadows","use_transparent_shadows","use_cast_shadows_only",
    "shadow_cast_alpha","use_only_shadow","shadow_only_type","use_cast_buffer_shadows","shadow_buffer_bias","use_ray_shadow_bias",
    "shadow_ray_bias","use_cast_approximate","light_group","use_light_group_exclusive","strand.uv_layer",)
    return surface_wire
#end SurfaceWire keys
#Volume keys
def VolumeKeys():
    volume  = \
    ("volume.density","volume.density_scale","volume.scattering","volume.asymmetry","volume.emission","volume.emission_color",
     "volume.reflection","volume.reflection_color","volume.transmission_color","volume.light_method","volume.use_external_shadows",
     "volume.use_light_cache","volume.cache_resolution","volume.ms_diffusion","volume.ms_spread","volume.ms_intensity",
     "volume.step_method","volume.step_size","volume.depth_threshold","transparency_method","use_raytrace","use_full_oversampling",
     "use_mist", "light_group","use_light_group_exclusive",)
    return volume
#end Volume keys
#Halo keys
def HaloKeys():
    halo  = \
    ("halo.size","halo.hardness","halo.seed","halo.add","halo.use_texture","halo.use_vertex_normal","halo.use_extreme_alpha","halo.use_shaded",
     "halo.use_soft","halo.use_ring","halo.ring_count","halo.use_lines","halo.line_count","halo.use_star","halo.star_tip_count",
     "halo.use_flare_mode","halo.flare_size","halo.flare_boost","halo.flare_seed","halo.flare_subflare_count","halo.flare_subflare_size",
     "alpha","diffuse_color","specular_color", "mirror_color", "strand.root_size","strand.tip_size","strand.size_min","strand.use_blender_units",                        
     "strand.use_tangent_shading","strand.shape","strand.width_fade","strand.blend_distance","strand.uv_layer",)    
    return halo
#end Halo keys
#String properties keys
def StringPropertiesKeys():
    string_properties  = \
    ("diffuse_shader", "specular_shader", "transparency_method", "raytrace_mirror.fade_to", "shadow_only_type",
     "volume.light_method","volume.step_method", "diffuse_ramp.blend", "diffuse_ramp.input", "diffuse_ramp.interpolation",
     "specular_ramp.blend", "specular_ramp.input", "specular_ramp.interpolation",  "object", "object.name",
     "texture_coords", "mapping", "mapping_x", "mapping_y", "mapping_z", "uv_layer", "uv_layer.name", "color_ramp.interpolation", 
     "point_density_color_ramp.interpolation",)    
    return string_properties
#end String properties keys
#Ramps properties keys
def RampsKeys(type_ramp):
    ramps  = \
    ["#1#_ramp.elements.position", "#1#_ramp.elements.color", "#1#_ramp.blend",   
     "#1#_ramp.input", "#1#_ramp.factor", "#1#_ramp.interpolation",]    
    count = 0
    for v in ramps:
        ramps[count] = v.replace("#1#", type_ramp) 
        count = count + 1
    if type_ramp == 'color' or type_ramp == 'point_density_color':
        exceptions = ("%s_ramp.input"%type_ramp, "%s_ramp.factor"%type_ramp, "%s_ramp.blend"%type_ramp,)
        for e in exceptions:
            ramps.remove(e)
    return ramps
#end Ramps properties keys
#Exceptions ramps properties keys
def ExceptionsRampsKeys():
    ramps  = (".blend", ".input", ".factor", ".interpolation",)    
    return ramps
def ExceptionsRampsKeys_2():
    ramps  = ("_blend", "_input", "_factor", ".interpolation",)    
    return ramps
def ExceptionsRampsKeys_3():
    ramps  = ("slot.texture.color_ramp.interpolation", "slot.texture.point_density.color_ramp.interpolation",)    
    return ramps
#end Exceptions ramps properties keys
#Textures properties keys
def MappingExportKeys():
    mapping  = ("texture_coords", "mapping", "mapping_x", "mapping_y", "mapping_z",
                "use_from_dupli", "use_from_original", "scale", "offset", )    
    return mapping
def InfluenceExportKeys():
    influence  = ("use_map_diffuse", "use_map_color_diffuse", "use_map_alpha", "use_map_translucency", "use_map_ambient",
                  "use_map_emit", "use_map_mirror", "use_map_raymir", "use_map_specular", "use_map_color_spec", 
                  "use_map_hardness", "use_map_normal", "use_map_warp", "use_map_displacement", "diffuse_factor",
                  "diffuse_color_factor", "alpha_factor", "translucency_factor", "specular_factor", "specular_color_factor",
                  "hardness_factor", "ambient_factor", "emit_factor", "mirror_factor", "raymir_factor", "normal_factor",
                  "warp_factor", "displacement_factor", "blend_type", "use_rgb_to_intensity", "color", "invert", "use_stencil",
                  "default_value", "bump_method", "bump_objectspace",)    
    return influence
def ColorsExportKeys():
    colors  = ("texture.use_color_ramp", "texture.factor_red", "texture.factor_green", "texture.factor_blue", 
                "texture.intensity", "texture.contrast", "texture.saturation", "texture.factor_blue",)    
    return colors
def BlendExportKeys():
    blend  = ("texture.progression", "texture.use_flip_axis",)    
    return blend
def CloudsExportKeys():
    clouds  = ("texture.cloud_type", "texture.noise_type", "texture.noise_basis", "texture.noise_scale",
               "texture.nabla", "texture.noise_depth", )    
    return clouds
def DistortedExportKeys():
    distorted  = ("texture.noise_distortion", "texture.noise_basis", "texture_distortion",
               "texture.nabla", "texture.noise_scale", )    
    return distorted
def MagicExportKeys():
    magic  = ("texture.noise_depth", "texture.turbulence",)    
    return magic
def MarbleExportKeys():
    marble  = ("texture.marble_type", "texture.noise_scale_2", "texture.noise_type", "texture.noise_basis",
               "texture.noise_scale", "texture.noise_depth", "texture.nabla", "texture.turbulence",)    
    return marble
def MusgraveExportKeys():
    musgrave  = ("texture.noise_basis", "texture.noise_scale", "texture.nabla", "texture.musgrave_type",
                 "texture.dimension_max", "texture.lacunarity", "texture.octaves", "texture.offset",
                 "texture.noise_intensity", "texture.gain",)    
    return musgrave
def StucciExportKeys():
    stucci  = ("texture.stucci_type", "texture.noise_type", "texture.noise_basis", 
               "texture.noise_scale", "texture.turbulence",)    
    return stucci
def VoronoiExportKeys():
    voronoi  = ("texture.distance_metric", "texture.minkovsky_exponent", "texture.color_mode", 
               "texture.noise_intensity", "texture.noise_scale", "texture.nabla", "",
                "texture.weight_1", "texture.weight_2", "texture.weight_3", "texture.weight_4",)    
    return voronoi
def WoodExportKeys():
    wood  = ("texture.noise_basis_2", "texture.wood_type", "texture.noise_type", "texture.noise_basis",
             "texture.noise_scale", "texture.nabla", "texture.turbulence", )    
    return wood
def PointExportKeys():
    point  = ("texture.point_density.use_turbulence", "texture.point_density.turbulence_influence", "texture.noise_basis",
              "texture.point_density.turbulence_scale", "texture.point_density.turbulence_depth", "texture.point_density.turbulence_strength", 
              "texture.point_density.point_source", "texture.point_density.particle_cache_space","texture.point_density.speed_scale",
              "texture.point_density.color_source", "texture.point_density.radius", "texture.point_density.falloff", 
              "texture.point_density.use_falloff_curve", "texture.point_density.vertex_cache_space", "texture.point_density.falloff_speed_scale",)    
    return point
def VoxelExportKeys():
    voxel  = ("texture.voxel_data.intensity", "texture.voxel_data.extension", "texture.voxel_data.interpolation", "texture.voxel_data.smoke_data_type",
              "texture.voxel_data.file_format",)    
    return voxel
def ImageExportKeys():
    image  = ("texture.extension", "texture.crop_min_x", "texture.crop_min_y", "texture.crop_max_x","texture.crop_max_y",
              "texture.repeat_x", "texture.repeat_y", "texture.use_mirror_x","texture.use_mirror_y",
              "texture.use_checker_even", "texture.use_checker_odd", "texture.checker_distance", "texture.use_alpha", 
              "texture.use_calculate_alpha", "texture.invert_alpha", "texture.use_flip_axis", "texture.use_normal_map",
              "texture.normal_map_space", "texture.use_derivative_map", "texture.use_mipmap", "texture.use_mipmap_gauss",
              "texture.use_interpolation","texture.filter_type","texture.filter_eccentricity","texture.filter_size",
              "texture.filter_probes", "texture.use_filter_size_min", "texture.image.source",
              "texture.image.generated_width", "texture.image.generated_height", "texture.image.generated_float", 
              "texture.image.generated_type", "texture.image.use_fields", "texture.image.use_premultiply", 
              "texture.image.field_order", "texture.image.frame_duration", "texture.image.frame_start", 
              "texture.image.frame_offset", "texture.image.fields_per_frame", "texture.image.use_auto_refresh", 
              "texture.image.use_cyclic",)    
    return image
#end Textures properties keys
#Render properties keys
def RenderInternalKeys():
    render_internal  = ("render_resolution_x", "render_resolution_y", "render_resolution_percentage", "render_pixel_aspect_x", "render_pixel_aspect_y",
                        "render_use_antialiasing", "render_antialiasing_samples", "render_use_full_sample", "render_filepath", "render_file_format",
                        "render_color_mode", "render_use_file_extension", "render_use_overwrite", "render_use_placeholder", "render_file_quality",)    
    return render_internal
def StandartValuesRenderInternalKeys():
    standart_render_internal  = {"render_resolution_x":512, "render_resolution_y":512, "render_resolution_percentage":100, "render_use_full_sample":False,
                                 "render_pixel_aspect_x":1.0, "render_pixel_aspect_y":1.0, "render_use_antialiasing":True, "render_antialiasing_samples":'16', 
                                 "render_filepath":'', "render_file_format":'JPEG',  "render_color_mode":'RGB', "render_use_file_extension":True, 
                                 "render_use_overwrite":True, "render_use_placeholder":False, "render_file_quality":100,}    
    return standart_render_internal
#end Render properties keys


