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
import bpy, os, shutil, sys
from . import environment, misc, materials, keys, ramps, textures
from copy import copy

#Create material only here
def MaterialExport(material_dict, api_functions):
    ctx_obj = eval(api_functions['context_object'])
    ctx_mat = eval(api_functions['context_material'])
    type_mat = eval(api_functions['type'])
    slots = api_functions['material_slots']
    slots = slots.replace("#1#", str(api_functions['material_slots'].replace("[#1#].material", "")) + ".__len__() - 1")
    mat_properties = [] 
    material_structure = ["# %s\n" % ("*"*128), "# Material name : %s \n" % material_dict['material_name'],
                          "# Created by : %s \n" %  material_dict['creator'],
                          "# Weblink : %s \n" %  material_dict['weblink'],
                          "# Email : %s \n" %  material_dict['email'],
                          "# Description : %s \n" %  material_dict['description'],
                          "# Key words : %s \n" %  material_dict['key_words'],
                          "# Created with Blender3D and BlenderShadersTools Next Gen Add-on\n",
                          "# %s\n" % ("*"*128),"\n","# Imports :\n", "import bpy, os\n","\n", "# Context :\n",
                          "ctx_obj = %s \n" % api_functions['context_object'],
                          "ctx_mat = %s \n" % api_functions['context_material'],
                          "type_mat = '%s'\n" % eval(api_functions['type']),
                          "\n","# Script Path :\n",
                          "mat_name = '%s'\n" % material_dict['material_name'],
                          "mat_creator = '%s'\n" % material_dict['creator'],
                          "!*-environnement_path-*!\n","\n","# Create Material :\n",
                          "def CreateMaterial(mat_name):\n","\t# Materials Values :\n",
                          "\tmat = %s\n" % api_functions['materials_new'].replace("#1#", "mat_name"),]

    if type_mat == 'SURFACE' or type_mat == 'WIRE':
        mat_properties = materials.SurfaceWireVolumeHalo(api_functions, keys.MaterialsPropertiesKeys(api_functions), keys.SurfaceWireKeys())
        for p in mat_properties:
            if p[2]:
                material_structure.append("\tmat.%s = '%s' \n" % (p[0], p[1]))
            else:
                material_structure.append("\tmat.%s = %s \n" % (p[0], p[1]))

        material_structure.append("\treturn mat\n\n")
        material_structure.append("%s\n" % api_functions['material_slot_add'])
        material_structure.append("%s = CreateMaterial('EXP_%s')\n" % (slots, material_dict['material_name']))

    elif type_mat == 'VOLUME':
        mat_properties = materials.SurfaceWireVolumeHalo(api_functions, keys.MaterialsPropertiesKeys(api_functions), keys.VolumeKeys())
        material_structure.append("\treturn mat\n\n")
        material_structure.append("%s\n" % api_functions['material_slot_add'])
        material_structure.append("%s = CreateMaterial('EXP_%s')\n" % (slots, material_dict['material_name']))
        material_structure.append("%s = '%s'\n" % (str(api_functions['type']), type_mat))
        material_structure.append("slots = %s\n" % slots)
        
        for p in mat_properties:
            if p[2]:
                material_structure.append("slots.%s = '%s' \n" % (p[0], p[1]))
            else:
                material_structure.append("slots.%s = %s \n" % (p[0], p[1]))
    
    elif type_mat == 'HALO':
        mat_properties = materials.SurfaceWireVolumeHalo(api_functions, keys.MaterialsPropertiesKeys(api_functions), keys.HaloKeys())
        material_structure.append("\treturn mat\n\n")
        material_structure.append("%s\n" % api_functions['material_slot_add'])
        material_structure.append("%s = CreateMaterial('EXP_%s')\n" % (slots, material_dict['material_name']))
        material_structure.append("%s = '%s'\n" % (str(api_functions['type']), type_mat))
        material_structure.append("slots = %s\n" % slots)
        
        for p in mat_properties:
            if p[2]:
                material_structure.append("slots.%s = '%s' \n" % (p[0], p[1]))
            else:
                material_structure.append("slots.%s = %s \n" % (p[0], p[1]))

    # i open and create export file:
    temp_path = os.path.join(material_dict['temp'], material_dict['material_name'])
    script_path = os.path.join(temp_path, "script.py")
    if os.path.exists(temp_path):
        try: misc.Clear(temp_path, 'files', 'all')
        except: print("$hadertools : error clean up folder : %s" % temp_path)
    else:
        try: os.makedirs(temp_path)
        except: print("$hadertools : error create folder : %s" % temp_path)
    
    # create script file:
    try:
        script_file = open(script_path, 'w',  encoding = "utf-8")
        for l in material_structure:
            script_file.write(l)
        
        script_file.close()
        print("$hadertools : material sctructure write in blex file.")
    except:
        print("$hadertools : error material sctructure not write in blex file.")
#end Create material only here
#Create ramps only here
def MaterialRampsExport(material_dict, api_functions, ramp_type):
    ctx_mat = eval(api_functions['context_material'])
    type_mat = eval(api_functions['type'])
    ramp_used = False
    ramp_properties = [] 
    ramp_structure = ["\n", "# Create ramps context :\n", "ramp = %s \n\n" % api_functions['context_material'],]

    if type_mat == 'SURFACE' or type_mat == 'WIRE':
        if eval(api_functions['use_diffuse_ramp']) and ramp_type == 'diffuse':
            ramp_used = True
            ramp_structure.append("# Create diffuse ramp context :\n")
            ramp_structure.append("%s = True\n" % api_functions['use_diffuse_ramp'].replace(api_functions['context_material'], "ramp"))
            type_ramp = 'diffuse'
            ramp_structure[1] =  ramp_structure[1].replace("#1#", type_ramp)
            for v in ramps.RampsPositions(api_functions, type_ramp, ''):
                ramp_structure.append(v.replace(api_functions['context_material'], "ramp"))
            ramp_properties = ramps.Ramps(api_functions, keys.RampsPropertiesKeys(api_functions), keys.RampsKeys(type_ramp), type_ramp, '')
        
        if eval(api_functions['use_specular_ramp']) and ramp_type == 'specular': 
            ramp_used = True
            if eval(api_functions['use_diffuse_ramp']):
                    ramp_structure = []
            ramp_structure.append("\n# Create specular ramp context :\n")
            ramp_structure.append("%s = True\n" % api_functions['use_specular_ramp'].replace(api_functions['context_material'], "ramp"))
            type_ramp = 'specular'
            ramp_structure[1] =  ramp_structure[1].replace("#1#", type_ramp)
            for v in ramps.RampsPositions(api_functions, type_ramp, ''):
                ramp_structure.append(v.replace(api_functions['context_material'], "ramp"))
            ramp_properties = ramps.Ramps(api_functions, keys.RampsPropertiesKeys(api_functions), keys.RampsKeys(type_ramp), type_ramp, '')

        for i in range(0, ramp_properties.__len__()):
            for k in keys.RampsKeys(type_ramp):
                exception = False
                for s in keys.StringPropertiesKeys():
                    if s.find(k) >= 0:
                        exception = True
                        break
                if exception:
                    ramp_structure.append("%s = '%s' \n" % (ramp_properties[str(i)][k][0].replace(api_functions['context_material'], "ramp"), ramp_properties[str(i)][k][1]))
                else:
                    ramp_structure.append("%s = %s \n" % (ramp_properties[str(i)][k][0].replace(api_functions['context_material'], "ramp"), ramp_properties[str(i)][k][1]))

    for v in keys.ExceptionsRampsKeys_2():                    
        ramps.RemoveElements(v, ramp_structure)        
    # i open and create export file:
    temp_path = os.path.join(material_dict['temp'], material_dict['material_name'])
    script_path = os.path.join(temp_path, "script.py")
    # create script file:
    if ramp_used:
        try:
            script_file = open(script_path, 'a',  encoding = "utf-8")
            for l in ramp_structure:
                script_file.write(l)
        
            script_file.close()
            print("$hadertools : ramps sctructure write in blex file.")
        except:
            print("$hadertools : error ramps sctructure not write in blex file.")
#end Create ramps only here
#Create texture ramps only here
def TextureRampsExport(material_dict, api_functions, type_ramp, idx_texture, texture_structure):
    ctx_texture = copy(api_functions['context_texture'].replace("#1#", str(idx_texture)))
    ctx_slot = copy(api_functions['texture_slots']) + "[%s]"%str(idx_texture)
    ramp_used = False
    
    if type_ramp == 'color': 
        ramp_used = True
        texture_structure.append("#colors ramp\n")
        for v in ramps.RampsPositions(api_functions, type_ramp, idx_texture):
            texture_structure.append(v.replace(ctx_slot, "slot"))
        ramp_properties = ramps.Ramps(api_functions, keys.RampsPropertiesKeys(api_functions), keys.RampsKeys(type_ramp), type_ramp, idx_texture)
    
    for i in range(0, ramp_properties.__len__()):
        for k in keys.RampsKeys(type_ramp):
            exception = False
            for s in keys.StringPropertiesKeys():
                if s.find(k) >= 0:
                    exception = True
                    break
            if exception:
                texture_structure.append("%s = '%s' \n" % (ramp_properties[str(i)][k][0].replace(ctx_slot, "slot"), ramp_properties[str(i)][k][1]))
            else:
                texture_structure.append("%s = %s \n" % (ramp_properties[str(i)][k][0].replace(ctx_slot, "slot"), ramp_properties[str(i)][k][1]))
            

    
    return texture_structure



#end Create texture ramps only here
#Textures only here
def TextureExport(material_dict, api_functions):
    texture_structure = ["\n", "# Create texture context :\n","ctx_texture_slots = %s\n" % api_functions['texture_slots'],
                         "ctx_mat = %s\n" % api_functions['context_material'],]
    ctx_mat = copy(api_functions['context_material'])
    ctx_texture = copy(api_functions['context_texture'])
    current_texture = eval(api_functions['texture_slots_values'])
    texture_idx = 0
    for t in range(0, current_texture.__len__()):
        if current_texture[t] != None:
            texture_used = copy(eval(api_functions['texture_slots_values_use'].replace("#1#", str(t))))
            texture_type = copy(eval(api_functions['texture_slots_values_texture_type'].replace("#1#", str(t))))            
            if texture_used :
                texture_structure.append("\n# Create %s texture :\n" % texture_type)
                #Add texture name here
                add_name_eval = "'" + eval(api_functions['texture_slots_texture_name'].replace("#1#", str(t))) + "'"
                add_type_eval = "'" + eval(api_functions['texture_slots_texture_type'].replace("#1#", str(t))) + "'"
                add_name = copy(api_functions['texture_slots_new'].replace("#1#", add_name_eval))
                add_name = add_name.replace("#2#", add_type_eval)
                texture_structure.append("new_texture = %s\n" % add_name)
                texture_structure.append("slot = %s\n" % api_functions['texture_slots_add'].replace(ctx_mat, "ctx_mat"))
                texture_structure.append("slot.texture = new_texture\n")

                #Here create texture slot context
                val = copy(ctx_texture.replace("#1#", str(texture_idx)))
                val = val.replace(api_functions['texture_slots'], "ctx_texture_slots")
                texture_structure.append("ctx_texture = %s \n" % val)

                #Use preview alpha bool
                preview = copy(api_functions['texture_use_preview_alpha'].replace("#1#", str(texture_idx)))
                preview_eval = eval(api_functions['texture_use_preview_alpha'].replace("#1#", str(t))) 
                preview = preview.replace(api_functions['texture_slots'], "ctx_texture_slots")
                texture_structure.append("%s = %s \n" % (preview, preview_eval))
                
                #Create mapping texture properties
                texture_structure = textures.MappingInfluenceColorsExport(api_functions, texture_structure, keys.MappingExportKeys(), t)
                #Create influence texture properties
                texture_structure = textures.MappingInfluenceColorsExport(api_functions, texture_structure, keys.InfluenceExportKeys(), t)
                #Create colors texture properties
                texture_structure = textures.MappingInfluenceColorsExport(api_functions, texture_structure, keys.ColorsExportKeys(), t)
                ramp_colors =  copy(api_functions['texture_use_color_ramp'].replace("#1#", str(t)))
                if eval(ramp_colors):
                    TextureRampsExport(material_dict, api_functions, 'color', t, texture_structure)
                
                #Now different type of texture
                if texture_type == 'BLEND':
                    print("BLEND")
                elif texture_type == 'CLOUDS':
                    print("CLOUDS")
                elif texture_type == 'DISTORTED_NOISE':
                    print("DISTORTED_NOISE")
                elif texture_type == 'ENVIRONMENT_MAP':
                    print("ENVIRONMENT_MAP")
                elif texture_type == 'IMAGE':
                    print("IMAGE")
                elif texture_type == 'MAGIC':
                    print("MAGIC")
                elif texture_type == 'MARBLE':
                    print("MARBLE")
                elif texture_type == 'MUSGRAVE':
                    print("MUSGRAVE")
                elif texture_type == 'NOISE':
                    print("NOISE")
                elif texture_type == 'POINT_DENSITY':
                    print("POINT_DENSITY")
                elif texture_type == 'STUCCI':
                    print("STUCCI")
                elif texture_type == 'VORONOI':
                    print("VORONOI")
                elif texture_type == 'VOXEL_DATA':
                    print("VOXEL_DATA")
                else:
                    print("WOOD")

                texture_idx = texture_idx + 1

    # i open and create export file:
    temp_path = os.path.join(material_dict['temp'], material_dict['material_name'])
    script_path = os.path.join(temp_path, "script.py")
    # create script file:
    try:
        script_file = open(script_path, 'a',  encoding = "utf-8")
        for l in texture_structure:
            script_file.write(l)
        
        script_file.close()
        print("$hadertools : texture sctructure write in blex file.")
    except:
        print("$hadertools : error texture sctructure not write in blex file.")

#end Textures only here








