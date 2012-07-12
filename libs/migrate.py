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
import bpy, os
from . import misc, keys, request, materials
from copy import copy

#Migrate SQLite Database V1->V2
def MigrateV1V2(path, api_functions, active_language, active_configuration, default_paths, idx):
    #Database stuff
    material_created = False
    #materials
    try:
        materials_values = request.DatabaseSelect(path, keys.OldMaterialsKeys(), "MATERIALS", "where Mat_Index=%s" %idx, 'one')
        #materials properties
        materials_values_element = []
        materials_values_final = []
        for e in materials_values: materials_values_final.append(e)
        for k in keys.OldMaterialsKeys(): materials_values_element.append(keys.OldMaterialsDict()[k])
        #materials tuples (Colors, Radius ...)
        for t in keys.OldMaterialsColorRadiusDict():
            materials_values_element.append(t)
            materials_values_final.append(str(request.DatabaseSelect(path, \
                keys.OldMaterialsColorRadiusDict()[t], "MATERIALS", "where Mat_Index=%s" %idx, 'one')))
        materials_values_final[1] = materials_values_final[1].replace("MAT_PRE_", "$T_")
        request.DatabaseInsert(default_paths['database'], materials_values_element, materials_values_final, "MATERIALS")
        material_created = True
    except:pass
    #end materials
    #materials ramps
    if material_created:
        try:
            temp_diffuse_values = request.DatabaseSelect(path, keys.OldDiffuseRampsKeys(), "DIFFUSE_RAMP", "where Dif_Num_material=%s" %idx, 'all')
            diffuse_values = []
            materials_ramps_values_element = []
            for k in keys.OldDiffuseRampsKeys():materials_ramps_values_element.append(keys.OldDiffuseRampsDict()[k])   
            for r in temp_diffuse_values:
                temp = []
                for k in r:
                    temp.append(k)
                for p in keys.OldDiffuseRampsColorDict():
                    v = request.DatabaseSelect(path,keys.OldDiffuseRampsColorDict()[p], "DIFFUSE_RAMP", "where Dif_Num_material=%s" %idx, 'all')
                    temp.append(str(v[0]))
                if not p in materials_ramps_values_element: materials_ramps_values_element.append(p)
                diffuse_values.append(copy(temp))
            for r in diffuse_values:request.DatabaseInsert(default_paths['database'], materials_ramps_values_element, r, "DIFFUSE_RAMPS")
        except:pass
        try:
            temp_specular_values = request.DatabaseSelect(path, keys.OldSpecularRampsKeys(), "SPECULAR_RAMP", "where Spe_Num_material=%s" %idx, 'all')
            specular_values = []
            materials_ramps_values_element = []
            for k in keys.OldSpecularRampsKeys():materials_ramps_values_element.append(keys.OldSpecularRampsDict()[k])   
            for r in temp_specular_values:
                temp = []
                for k in r:
                    temp.append(k)
                for p in keys.OldSpecularRampsColorDict():
                    v = request.DatabaseSelect(path,keys.OldSpecularRampsColorDict()[p], "SPECULAR_RAMP", "where Spe_Num_Material=%s" %idx, 'all')
                    temp.append(str(v[0]))
                if not p in materials_ramps_values_element: materials_ramps_values_element.append(p)
                specular_values.append(copy(temp))
            for r in specular_values:request.DatabaseInsert(default_paths['database'], materials_ramps_values_element, r, "SPECULAR_RAMPS")
        except:pass
    #end materials ramps






    '''

        try: textures_values = request.DatabaseSelect(path, keys.OldTexturesKeys(), "TEXTURES", "where Mat_Idx=%s" %idx, 'all')
        except:pass
        try: imageuv_values = request.DatabaseSelect(path, keys.OldImageUvKeys(), "IMAGE_UV", "where Idx_Texture=%s" %textures_values[0][0], 'all')
        except:pass
    try: colors_values = request.DatabaseSelect(path, keys.OldColorRampsKeys(), "COLORS_RAMP", "where Col_Num_material=%s" %idx, 'all')
    except: pass
    try: point_values = request.DatabaseSelect(path, keys.OldPointDensityRampsKeys(), "POINTDENSITY_RAMP", "where Poi_Num_material=%s" %idx, 'all')
    except: pass
    try: render_values = request.DatabaseSelect(path, keys.OldRenderKeys(), "RENDER", "where Mat_Index=%s" %idx, 'all')
    except: pass
    #end Database stuff
    '''
    #Here 
#print(materials_values)

        


#end Migrate SQLite Database V1->V2
