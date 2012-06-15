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

def ShowCredits(credits_key):
    #Imports & external libs:
    try:
        import bpy, os, textwrap
    except:
        print("$hadertools : credits import error")
    #end Imports & external libs:
    credits_list = []
    credits_row = []

    title_row = credits_key['function'].capitalize() + " :"
    title_row = title_row.replace("_", " and ")
    name_row = credits_key['name'].rstrip(",")

    if len(name_row) >= 35:
        wrap_text = textwrap.wrap(name_row,35)
        count = 0
        for v in wrap_text:
            credits_row = []
            if count == 0:
                count = 1
                credits_row.append(title_row)
                credits_row.append(v)
            else:
                credits_row.append('')
                credits_row.append(v)
            
            credits_list.append(credits_row)
    else:
        credits_row.append(title_row)
        credits_row.append(name_row)
        credits_list.append(credits_row)
    
    return credits_list
    
    
    
    
    