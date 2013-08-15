# ##### BEGIN CC LICENSE BLOCK #####
#
# This work is licensed under a 
# Creative Commons Attribution 3.0 
# Unported (CC BY 3.0) License : 
#
# More details here : http://creativecommons.org/licenses/by/3.0/deed.en
#
# ##### END CC LICENSE BLOCK #####

# <pep8-80 compliant>
#-*- coding: utf-8 -*-

import bpy, os, webbrowser

def help_me(app_path, active_language_name):
    #I open help file:
    if '(French)' in active_language_name: active_language_name = 'French'
    elif '(English)' in active_language_name: active_language_name = 'English'
        
    url = "file://" + os.path.join(app_path, "html", active_language_name, "index.html")
    webbrowser.open_new(url)       
