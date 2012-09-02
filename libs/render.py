# ##### BEGIN GPL LICENSE BLOCK #####
#
# This work is licensed under a Creative 
# Commons Attribution-NonCommercial-ShareAlike 
# 3.0 Unported License : 
#
# More details here : http://creativecommons.org/licenses/by-nc-sa/3.0/deed.fr
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>
import bpy, os, shutil
from . import misc, keys
from copy import copy

def PreviewRenderInternal(api_functions, active_configuration, material_dict):
    ctx_render = api_functions['context_render']
    preview_name = "%s_%s_%s_preview.jpg" % (material_dict['filename'].replace(".blex", ''), material_dict['material_name'], material_dict['creator'])
    path_preview = material_dict['filepath'].replace(material_dict['filepath'].split(os.sep)[-1], preview_name)
    path_preview = misc.DoubleSlash(path_preview)
    
    save_render_configuration = {}
    standart_values = keys.StandartValuesRenderInternalKeys()
    
    if not os.path.exists(preview_name):
        for p in keys.RenderInternalKeys():
            save_render_configuration[p] = eval(api_functions[p]) 
    
        for p in keys.RenderInternalKeys():
            if p == 'render_resolution_x':standart_values[p] = active_configuration['resolution_default_x']
            if p == 'render_resolution_y':standart_values[p] = active_configuration['resolution_default_y']
            if p == 'render_filepath':standart_values[p] = path_preview
            if type(eval(api_functions[p])).__name__ == 'str': 
                exec("%s = '%s'" % (str(api_functions[p]), str(standart_values[p])))
            else: exec("%s = %s" % (str(api_functions[p]), str(standart_values[p])))
        
        eval(api_functions['render_render'])
        save_render = api_functions['texture_image_save_as'].replace("#1#", "'Render Result'")
        save_render = save_render.replace("#2#", "'%s'" %path_preview)
        eval(save_render)

        for p in keys.RenderInternalKeys():
            if type(eval(api_functions[p])).__name__ == 'str': 
                exec("%s = '%s'" % (str(api_functions[p]), str(save_render_configuration[p])))
            else: exec("%s = %s" % (str(api_functions[p]), str(save_render_configuration[p])))

         



