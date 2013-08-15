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

import bpy, os, platform

def OpenViewer(program_parameters):
    if platform.system() == 'Darwin': os.popen("open -n -a '%s' --args '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s'" %  program_parameters)
    else: os.popen('"%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' %  program_parameters)

