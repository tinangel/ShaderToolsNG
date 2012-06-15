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

def DeZip(app_path, active_configuration, zip_path):
    #Imports & external libs:
    try:
        import bpy, os, zipfile, platform, shutil
    except:
        print("#ShaderToolsNG : error import dezip")
    #end Imports & external libs:
    #Copy zip_file & dezip:
    try:
        zip_file = zip_path.replace("#addon#", app_path)
        zip_in_zip_folder = os.path.join(active_configuration['zip_folder'].replace("#addon#", app_path), zip_file.split(os.path.sep)[-1] + ".zip")
        if os.path.exists(zip_in_zip_folder):
            os.remove(zip_in_zip_folder)
        shutil.copy2(zip_file, zip_in_zip_folder)

        zfile = zipfile.ZipFile(zip_in_zip_folder, 'r')
        for z in zfile.namelist():
            if os.path.isdir(z):
                try: 
                    os.makedirs(os.path.join(active_configuration['temp_folder'].replace("#addon#", app_path), z))
                except: 
                    pass
            else:
                try: 
                    os.makedirs(os.path.join(active_configuration['temp_folder'].replace("#addon#", app_path), os.path.dirname(z)))
                except: pass
                data = zfile.read(z)
                fp = open(os.path.join(active_configuration['temp_folder'].replace("#addon#", app_path), z), "wb")
                fp.write(data)
                fp.close()
            zfile.close()
            return True
    except:
        print("#ShaderToolsNG : error dezip file")
        return False
    #end Copy zip_file & dezip:

