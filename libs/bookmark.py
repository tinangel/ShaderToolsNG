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

def VerifyBookmark(bookmark_path, bookmark_folder_path, bookmark_folder_name):
    #Imports & external libs:
    try:
        import bpy, os, platform, shutil, sys
        from . import environment, request, misc
        print(misc.ConsoleError("bookmark import ", 1, True))
    except:
        print(misc.ConsoleError("bookmark import ", 1, False))
    #end Imports & external libs:
    #Save the bookmarks file:
    try:
        bookmark_path_save = bookmark_path + "_2"
        if not os.path.exists(bookmark_path):
            bookmarks_file = open(bookmark_path,'w', encoding = "utf-8")
            bookmarks_file.close()

        if os.path.exists(bookmark_path_save):
            os.remove(bookmark_path_save)

        shutil.copy2(bookmark_path, bookmark_path_save)
        print(misc.ConsoleError("bookmark save ", 1, True))
    except:
        print(misc.ConsoleError("bookmark save ", 1, False))
    #end Save the bookmarks file:
    #Create bookmark material folder:
    try:
        if not os.path.exists(bookmark_folder_path):
            os.makedirs(bookmark_folder_path)
        print(misc.ConsoleError("bookmark folder ", 1, True))
    except:
        print(misc.ConsoleError("bookmark folder ", 1, False))
    #end Create bookmark material folder:
    #Check the bookmarks file:
    try:
        bookmarks_file = open(bookmark_path,'r', encoding = "utf-8")
        bookmarks_list = bookmarks_file.readlines()
        bookmarks_new_list = []
        update = True
        bookmarks_flag = False
        for v in bookmarks_list:
            if bookmark_folder_path in v:
                update = False

            if "[Bookmarks]" in v:
                bookmarks_flag = True

        if update and bookmarks_flag:
            for v in bookmarks_list:
                bookmarks_new_list.append(v)
                if "[Bookmarks]" in v:
                    bookmarks_new_list.append(bookmark_folder_path + "\n") 

        if update and bookmarks_flag == False:
            bookmarks_new_list.append("[Bookmarks]\n")
            bookmarks_new_list.append(bookmark_folder_path + "\n")
            for v in bookmarks_list:
                bookmarks_new_list.append(v)
    
        if update == False:
            bookmarks_new_list = bookmarks_list
        
        bookmarks_file.close()
        os.remove(bookmark_path)
        new_bookmarks_file = open(bookmark_path, 'w', encoding = "utf-8")
        for v in bookmarks_new_list: 
            new_bookmarks_file.write(v)
        print(misc.ConsoleError("bookmark update ", 1, True))        
        if update:
            return True
        else:
            return False
    except:
        print(misc.ConsoleError("bookmark update ", 1, False))
        return False
    #end Check the bookmarks file:




