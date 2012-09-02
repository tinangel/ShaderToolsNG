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
import bpy, os
from . import misc, keys, request, materials
from copy import copy

#Migrate materials ramps
def MigrateV1V2MaterialRamps(materials_ramps_properties):
    temp_current_ramps_values = materials_ramps_properties[0]
    current_ramps_values = []
    materials_ramps_values_element = []
    for k in materials_ramps_properties[1]:materials_ramps_values_element.append(materials_ramps_properties[2][k])   
    c = 0
    for r in temp_current_ramps_values:
        temp = []
        for k in r: temp.append(k)
        for p in materials_ramps_properties[3]:
            v = materials_ramps_properties[4]
            temp.append(str(v[c]))
        if not p in materials_ramps_values_element: materials_ramps_values_element.append(p)
        current_ramps_values.append(copy(temp))
        c = c + 1
    for r in current_ramps_values:request.DatabaseInsert(materials_ramps_properties[6]['database'], materials_ramps_values_element, r, materials_ramps_properties[5])
#end Migrate materials ramps

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
        #try:
        textures_values = request.DatabaseSelect(path, keys.OldTexturesKeys(), "TEXTURES", "where Mat_Idx=%s" %idx, 'all')
        textures_values_element = []
        textures_values_final = []
        if type(textures_values).__name__ != 'NoneType' and type(textures_values).__name__ != 'bool': 
                for v in textures_values:
                    textures_values_element = []
                    textures_values_element_2 = []
                    textures_values_final = []
                    # create a new list with different only textures type properties :
                    if not v[2] == 'NONE':
                        for k in keys.OldInfoTextureMigrateKeys(): textures_values_element.append(k)
                        for k in keys.OldMappingMigrateKeys(): textures_values_element.append(k)
                        for k in keys.OldInfluenceMigrateKeys(): textures_values_element.append(k)
                        for k in keys.OldColorsMigrateKeys(): textures_values_element.append(k)
                        if v[2] == 'BLEND': 
                            for k in keys.OldBlendMigrateKeys(): textures_values_element.append(k)
                        elif v[2] == 'NOISE': None 
                        elif v[2] == 'CLOUDS': 
                            for k in keys.OldCloudsMigrateKeys(): textures_values_element.append(k)
                        elif v[2] == 'DISTORTED_NOISE': 
                            for k in keys.OldDistortedMigrateKeys(): textures_values_element.append(k)
                        elif v[2] == 'MAGIC':
                            for k in keys.OldMagicMigrateKeys(): textures_values_element.append(k)
                        elif v[2] == 'MARBLE': 
                            for k in keys.OldMarbleMigrateKeys(): textures_values_element.append(k)
                        elif v[2] == 'MUSGRAVE':
                            for k in keys.OldMusgraveMigrateKeys(): textures_values_element.append(k)
                        elif v[2] == 'STUCCI':
                            for k in keys.OldStucciMigrateKeys(): textures_values_element.append(k)
                        elif v[2] == 'VORONOI': 
                            for k in keys.OldVoronoiMigrateKeys(): textures_values_element.append(k)
                        elif v[2] == 'WOOD': 
                            for k in keys.OldWoodMigrateKeys(): textures_values_element.append(k)
                        elif v[2] == 'POINT_DENSITY': 
                            for k in keys.OldPointMigrateKeys(): textures_values_element.append(k)
                        elif v[2] == 'IMAGE': None
                        elif v[2] == 'ENVIRONMENT_MAP': None
                        else: 
                            for k in keys.OldVoxelMigrateKeys(): textures_values_element.append(k)
                        
                        req_final = request.DatabaseSelect(path, textures_values_element , "TEXTURES", "where Tex_Index = %s" %v[0], 'one')
                        #here textures current properties 
                        for t in req_final:                     
                            textures_values_final.append(t)
                        for e in textures_values_element: textures_values_element_2.append(keys.OldTexturesDict()[e])
                        #here textures specials properties (scale, influence colors, scale)
                        for p in keys.OldTexturesColorVectorDict():
                            textures_values_element_2.append(p)
                            textures_values_final.append(str(request.DatabaseSelect(path, keys.OldTexturesColorVectorDict()[p], "TEXTURES", "where Tex_Index=%s"  %v[0], 'one')))
                        #here textures images
                        imageuv_values = request.DatabaseSelect(path, keys.OldImageUvKeys(), "IMAGE_UV", "where Idx_Texture=%s" % v[0], 'one')
                        if not imageuv_values == [] and type(imageuv_values).__name__ != 'NoneType': 
                            for i in keys.OldImageUvKeys(): textures_values_element_2.append(keys.OldImageUvDict()[i])
                            for u in range(0, keys.OldImageUvKeys().__len__()): textures_values_final.append( imageuv_values[u])
                        request.DatabaseInsert(default_paths['database'], textures_values_element_2, textures_values_final, "TEXTURES")
                        misc.LogAndPrintError((active_languages['menu_error_error038'] % (str(v[2]),str(materials_values[1])), active_languages['menu_error_error038'] % (str(v[2]),str(materials_values[1]))))
        #except: misc.LogAndPrintError(((active_languages['menu_error_error039'] %  materials_values[1]), active_languages['menu_error_error039'] % materials_values[1]))
    #end textures
    #informations  
        try:
            informations_values = request.DatabaseSelect(path, keys.OldInformationsKeys(), "INFORMATIONS", "where Mat_Index=%s" %idx, 'one')
            #informations properties
            informations_values_element = []
            informations_values_final = []
            for v in informations_values:  informations_values_final.append(v)
            for e in keys.OldInformationsKeys(): informations_values_element.append(keys.OldInformationsDict()[e])
            request.DatabaseInsert(default_paths['database'], informations_values_element, informations_values_final, "INFORMATIONS")
            misc.LogAndPrintError((active_languages['menu_error_error048'] % materials_values[1], active_languages['menu_error_error048'] % materials_values[1]))
        except: misc.LogAndPrintError((active_languages['menu_error_error049'] % materials_values[1], active_languages['menu_error_error049'] % materials_values[1]))
    #end informations
    
#end Migrate SQLite Database V1->V2
