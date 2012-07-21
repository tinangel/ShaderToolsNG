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

#Migrate materials ramps
def MigrateV1V2MaterialRamps(materials_ramps_properties):
    temp_current_ramps_values = materials_ramps_properties[0]
    current_ramps_values = []
    materials_ramps_values_element = []
    for k in materials_ramps_properties[1]:materials_ramps_values_element.append(materials_ramps_properties[2][k])   
    for r in temp_current_ramps_values:
        temp = []
        for k in r:  temp.append(k)
        for p in materials_ramps_properties[3]:
            v = materials_ramps_properties[4]
            temp.append(str(v[0]))
        if not p in materials_ramps_values_element: materials_ramps_values_element.append(p)
        current_ramps_values.append(copy(temp))
    for r in current_ramps_values:request.DatabaseInsert(materials_ramps_properties[6]['database'], materials_ramps_values_element, r, materials_ramps_properties[5])
#end Migrate materials ramps

#Migrate textures  influence colors/offset/scale
def MigrateV1V2TexturesIncluenceOffsetScale(idx, textures_specials_properties):
     return request.DatabaseSelect(path, textures_specials_properties, "TEXTURES", "where Mat_Idx=%s" %idx, 'one')

#Migrate SQLite Database V1->V2
def MigrateV1V2(path, api_functions, active_languages, active_configuration, default_paths, idx):
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
        misc.LogAndPrintError((active_languages['menu_error_error035'] % (materials_values[1]),  active_languages['menu_error_error035'] % (materials_values[1])))
    except: misc.LogAndPrintError((active_languages['menu_error_error033'] % (materials_values[1]),  active_languages['menu_error_error033'] % (materials_values[1])))
    #end materials
    #materials ramps
    if material_created:
        try: #Diffuse ramp migration
            materials_ramps_properties = \
                (
                 request.DatabaseSelect(path, keys.OldDiffuseRampsKeys(), "DIFFUSE_RAMP", "where Dif_Num_material=%s" %idx, 'all'),
                 keys.OldDiffuseRampsKeys(), keys.OldDiffuseRampsDict(), keys.OldDiffuseRampsColorDict(),
                 request.DatabaseSelect(path,keys.OldDiffuseRampsColorDict()['diffuse_ramp_elements_color'], "DIFFUSE_RAMP", "where Dif_Num_material=%s" %idx, 'all'),
                 "DIFFUSE_RAMPS", default_paths,
                )
            if  not materials_ramps_properties[0] == []: 
                MigrateV1V2MaterialRamps(materials_ramps_properties)
                misc.LogAndPrintError((active_languages['menu_error_error036'] % ("diffuse ramps",materials_values[1]),  active_languages['menu_error_error036'] % ("diffuse ramps",materials_values[1])))
        except: misc.LogAndPrintError((active_languages['menu_error_error034'] % ("diffuse ramps",materials_values[1]),  active_languages['menu_error_error034'] % ("diffuse ramps",materials_values[1])))
        try: #Specular ramp migration
            materials_ramps_properties = \
                (
                 request.DatabaseSelect(path, keys.OldSpecularRampsKeys(), "SPECULAR_RAMP", "where Spe_Num_material=%s" %idx, 'all'),
                 keys.OldSpecularRampsKeys(), keys.OldSpecularRampsDict(), keys.OldSpecularRampsColorDict(),
                 request.DatabaseSelect(path,keys.OldSpecularRampsColorDict()['specular_ramp_elements_color'], "SPECULAR_RAMP", "where Spe_Num_Material=%s" %idx, 'all'),
                 "SPECULAR_RAMPS", default_paths,
                 )
            if  not materials_ramps_properties[0] == []: 
                MigrateV1V2MaterialRamps(materials_ramps_properties)
                misc.LogAndPrintError((active_languages['menu_error_error036'] % ("specular ramps",materials_values[1]),  active_languages['menu_error_error036'] % ("specular ramps",materials_values[1])))
        except: misc.LogAndPrintError((active_languages['menu_error_error034'] % ("specular ramps",materials_values[1]),  active_languages['menu_error_error034'] % ("specular ramps",materials_values[1])))
        try: #Color ramp migration
            materials_ramps_properties = \
                (
                 request.DatabaseSelect(path, keys.OldColorRampsKeys(), "COLORS_RAMP", "where Col_Num_Material=%s" %idx, 'all'),
                 keys.OldColorRampsKeys(), keys.OldColorRampsDict(), keys.OldColorRampsColorDict(),
                 request.DatabaseSelect(path,keys.OldColorRampsColorDict()['color_ramp_elements_color'], "COLORS_RAMP", "where Col_Num_Material=%s" %idx, 'all'),
                 "COLOR_RAMPS", default_paths,
                 )
            if  not materials_ramps_properties[0] == []: 
                MigrateV1V2MaterialRamps(materials_ramps_properties)
                misc.LogAndPrintError((active_languages['menu_error_error036'] % ("color ramps",materials_values[1]),  active_languages['menu_error_error036'] % ("color ramps",materials_values[1])))
        except: misc.LogAndPrintError((active_languages['menu_error_error034'] % ("color ramps",materials_values[1]),  active_languages['menu_error_error034'] % ("color ramps",materials_values[1])))
        try: #PointDensity ramp migration
            materials_ramps_properties = \
                (
                 request.DatabaseSelect(path, keys.OldPointDensityRampsKeys(), "POINTDENSITY_RAMP", "where Poi_Num_Material=%s" %idx, 'all'),
                 keys.OldPointDensityRampsKeys(), keys.OldPointDensityRampsDict(), keys.OldPointDensityRampsColorDict(),
                 request.DatabaseSelect(path,keys.OldPointDensityRampsColorDict()['point_density_ramp_elements_color'], "POINTDENSITY_RAMP", "where Poi_Num_Material=%s" %idx, 'all'),
                 "POINTDENSITY_RAMPS", default_paths,
                 )
            if  not materials_ramps_properties[0] == []: 
                MigrateV1V2MaterialRamps(materials_ramps_properties)
                misc.LogAndPrintError((active_languages['menu_error_error036'] % ("point density ramps",materials_values[1]),  active_languages['menu_error_error036'] % ("point density ramps",materials_values[1])))
        except: misc.LogAndPrintError((active_languages['menu_error_error034'] % ("point density ramps",materials_values[1]),  active_languages['menu_error_error034'] % ("point density ramps",materials_values[1])))
    #end materials ramps
    #preview render 
        try:
            render_values = request.DatabaseSelect(path, keys.OldRenderKeys(), "RENDER", "where Mat_Index=%s" %idx, 'one')
            #render properties
            render_values_element = []
            render_values_final = []
            for v in render_values:  render_values_final.append(v)
            for e in keys.OldRenderKeys(): render_values_element.append(keys.OldRenderDict()[e])
            request.DatabaseInsert(default_paths['database'], render_values_element, render_values_final, "RENDER")
            misc.LogAndPrintError((active_languages['menu_error_error036'] % ("preview render",materials_values[1]), active_languages['menu_error_error036'] % ("preview render",materials_values[1])))
        except: misc.LogAndPrintError((active_languages['menu_error_error034'] % ("preview render",materials_values[1]), active_languages['menu_error_error034'] % ("preview render",materials_values[1])))
    #end preview render 
    #textures
        textures_values = request.DatabaseSelect(path, keys.OldTexturesKeys(), "TEXTURES", "where Mat_Idx=%s" %idx, 'all')
        #textures properties
        textures_values_element = []
        textures_values_final = []
        if type(textures_values).__name__ != 'NoneType' and type(textures_values).__name__ != 'bool': 
            for v in textures_values: 
                textures_values_element = []
                textures_values_final = []
                #here textures current properties 
                for t in v: textures_values_final.append(t)
                for e in keys.OldTexturesKeys(): textures_values_element.append(keys.OldTexturesDict()[e])
                #here textures specials properties (scale, influence colors, scale)
                for p in keys.OldTexturesColorVectorDict():
                    textures_values_element.append(p)
                    textures_values_final.append(str(request.DatabaseSelect(path, keys.OldTexturesColorVectorDict()[p], "TEXTURES", "where Mat_Idx=%s" %idx, 'one')))
                request.DatabaseInsert(default_paths['database'], textures_values_element, textures_values_final, "TEXTURES")
    #end textures






    '''

        try: textures_values = request.DatabaseSelect(path, keys.OldTexturesKeys(), "TEXTURES", "where Mat_Idx=%s" %idx, 'all')
        except:pass
        try: imageuv_values = request.DatabaseSelect(path, keys.OldImageUvKeys(), "IMAGE_UV", "where Idx_Texture=%s" %textures_values[0][0], 'all')
        except:pass
    #end Database stuff
    '''
    #Here 
#print(materials_values)




#end Migrate SQLite Database V1->V2
