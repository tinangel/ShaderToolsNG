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
from . import environment, misc, materials, keys, ramps

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
def RampsExport(material_dict, api_functions, idx_texture):
    ctx_mat = eval(api_functions['context_material'])
    type_mat = eval(api_functions['type'])
    ramp_used = False
    ramp_properties = [] 
    ramp_structure = ["\n", "# Create #1# ramp context :\n", "ramp = %s \n" % api_functions['context_material'],
                      "%s = True\n" % api_functions['use_diffuse_ramp'].replace(api_functions['context_material'], "ramp"),
                      "ramp_min_position = 0.0\n", "ramp_max_position = 1.0\n\n",]

    if type_mat == 'SURFACE' or type_mat == 'WIRE':
        if eval(api_functions["use_diffuse_ramp"]):
            ramp_used = True
            type_ramp = 'diffuse'
            ramp_structure[1] =  ramp_structure[1].replace("#1#", type_ramp)
            ramp_properties = ramps.Ramps(api_functions, keys.RampsPropertiesKeys(api_functions), keys.RampsKeys(type_ramp), type_ramp)
        
        if eval(api_functions["use_specular_ramp"]): 
            ramp_used = True
            type_ramp = 'specular'
            ramp_structure[1] =  ramp_structure[1].replace("#1#", type_ramp)
            ramp_properties = ramps.Ramps(api_functions, keys.RampsPropertiesKeys(api_functions), keys.RampsKeys(type_ramp), type_ramp)

        for i in range(0, ramp_properties.__len__()):
            if i == 0:
                for k in keys.RampsKeys("diffuse"):
                    exception = False
                    for s in keys.StringPropertiesKeys():
                        if s.find(k) >= 0:
                            exception = True
                            break
                    if exception:
                        ramp_structure.append("%s = '%s' \n" % (ramp_properties[str(i)][k][0].replace(api_functions['context_material'], "ramp"), ramp_properties[str(i)][k][1]))
                    else:
                        ramp_structure.append("%s = %s \n" % (ramp_properties[str(i)][k][0].replace(api_functions['context_material'], "ramp"), ramp_properties[str(i)][k][1]))
            else:
                for p in ramp_properties[str(i)]:
                    ramp_structure.append("%s = %s \n" % (ramp_properties[str(i)][p][0].replace(api_functions['context_material'], "ramp"), ramp_properties[str(i)][p][1]))

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