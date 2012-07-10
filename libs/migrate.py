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
    try: materials_values = request.DatabaseSelect(path, keys.OldMaterialsKeys(), "MATERIALS", "where Mat_Index=%s" %idx, 'all')
    except:pass
    try: textures_values = request.DatabaseSelect(path, keys.OldTexturesKeys(), "TEXTURES", "where Mat_Idx=%s" %idx, 'all')
    except:pass
    try: imageuv_values = request.DatabaseSelect(path, keys.OldImageUvKeys(), "IMAGE_UV", "where Idx_Texture=%s" %textures_values[0][0], 'all')
    except:pass
    try: diffuse_values = request.DatabaseSelect(path, keys.OldDiffuseRampsKeys(), "DIFFUSE_RAMP", "where Dif_Num_material=%s" %idx, 'all')
    except:pass
    try: specular_values = request.DatabaseSelect(path, keys.OldSpecularRampsKeys(), "SPECULAR_RAMP", "where Spe_Num_material=%s" %idx, 'all')
    except:pass
    try: colors_values = request.DatabaseSelect(path, keys.OldColorRampsKeys(), "COLORS_RAMP", "where Col_Num_material=%s" %idx, 'all')
    except: pass
    try: point_values = request.DatabaseSelect(path, keys.OldPointDensityRampsKeys(), "POINTDENSITY_RAMP", "where Poi_Num_material=%s" %idx, 'all')
    except: pass
    try: render_values = request.DatabaseSelect(path, keys.OldRenderKeys(), "RENDER", "where Mat_Index=%s" %idx, 'all')
    except: pass
    #end Database stuff

    #Here 


        


#end Migrate SQLite Database V1->V2
