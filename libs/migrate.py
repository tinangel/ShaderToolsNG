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
    materials_values = request.DatabaseSelect(path, keys.OldMaterialsKeys(), "MATERIALS", "where Mat_Index=%s" %idx, 'all')
    textures_values = request.DatabaseSelect(path, keys.OldTexturesKeys(), "TEXTURES", "", 'all')
    imageuv_values = request.DatabaseSelect(path, keys.OldImageUvKeys(), "IMAGE_UV", "", 'all')
    diffuse_values = request.DatabaseSelect(path, keys.OldDiffuseRampsKeys(), "DIFFUSE_RAMP", "", 'all')
    specular_values = request.DatabaseSelect(path, keys.OldSpecularRampsKeys(), "SPECULAR_RAMP", "", 'all')
    colors_values = request.DatabaseSelect(path, keys.OldColorRampsKeys(), "COLORS_RAMP", "", 'all')
    point_values = request.DatabaseSelect(path, keys.OldPointDensityRampsKeys(), "POINTDENSITY_RAMP", "", 'all')
    render_values = request.DatabaseSelect(path, keys.OldRenderKeys(), "RENDER", "", 'all')


    #print(materials_values[0][1])
    return 0
#end Migrate SQLite Database V1->V2
