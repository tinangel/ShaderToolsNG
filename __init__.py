# ##### BEGIN CC LICENSE BLOCK #####
#
# This work is licensed under a Creative 
# Commons Attribution-NonCommercial-ShareAlike 
# 3.0 Unported License : 
#
# More details here : http://creativecommons.org/licenses/by-nc-sa/3.0/deed.fr
#
# ##### END CC LICENSE BLOCK #####

# <pep8-80 compliant>
#-*- coding: utf-8 -*-

bl_info = {
    "name": "ShaderTools Next Gen",
    "author": "GRETETE Karim (Tinangel)",
    "version": (0, 9, 6),
    "blender": (2, 6, 0),
    "api": 41098,
    "location": "User Preferences",
    "description": "Shader tools for blender",
    "warning": "Beta version",
    "wiki_url": "http://noadress",
    "tracker_url": "",
    "support": 'COMMUNITY',
    "category": "System",}

print("*"*78)
print("*" + " "*22 + "Shader Tools Next Gen - Console" + " "*23 + "*")
print("*"*78)

#Imports & external libs:
try:
    import bpy, sqlite3, os, platform, locale, shutil, sys, time, shader_tools_ng.libs, threading,  webbrowser
    from shader_tools_ng.libs import *
    print(misc.ConsoleError("Import external module ", 0, True))
except: print(misc.ConsoleError("Import external module ", 0, False))

try:
    misc.LogError("", True)
    misc.LogError("*"*78, True)
    misc.LogError("*" + " "*22 + "Shader Tools Next Gen - Console" + " "*23 + "*", False)
    misc.LogError("*"*78, False)
    blender_version = str(bpy.app.version[0]) + "." + str(bpy.app.version[1]) + str(bpy.app.version[2])
    default_paths = environment.DefaultPaths()
    api_functions = environment.ApiDatas(default_paths['apis_database'], blender_version)
    configurations_config = environment.ConfigurationsDatas(default_paths['configs_database'], False)
    languages_config = environment.LanguagesDatas(default_paths['languages_database'])
    active_configuration = environment.ActiveConfigurations(configurations_config)
    active_languages = environment.ActiveLanguage(languages_config, active_configuration['language'])
    about_config = environment.AboutDatas(default_paths['database'])
    active_categories = environment.MaterialsCatergories(active_languages)
    names_config = environment.ConfigurationsNames(configurations_config)
    options_actions = environment.ConfigurationsOptions(active_languages)
    names_languages = environment.LanguagesNames(languages_config)
    space_access_name = active_languages['space_access_name'] + " "
    active_history = history.CurrentHistory(default_paths,  active_configuration, api_functions, active_languages)
    default_paths = environment.ConvertDefaultPaths(default_paths,  active_configuration)
    print(misc.ConsoleError("Globals ", 0, True))
except: print(misc.ConsoleError("Globals ", 0, False))

#Functions
conf_current_name = ""
conf_current_idx = 1
database_stuff = False
inf_current_weblink = False
progress_bar = False
#Tests & verifications
bookmarks_folder_path = os.path.join(default_paths['app'], active_languages['menu_bookmarks_name'])
update = checkup.MakeCheckup(default_paths['database'], default_paths['configs_database'], default_paths['bookmarks'], 
                             bookmarks_folder_path, active_languages['menu_bookmarks_name'], active_configuration, default_paths['app'], 
                             languages_config,  default_paths)
lauch_progress_bar = threading.Thread(None, open.CreateThumbnails, "Create_thumbnails", (default_paths,  active_configuration, api_functions, active_languages, False, ), {})
lauch_progress_bar.start()
#Panel and buttons 
def ctx_active_object():
    global api_functions
    ctx_active_object = False
    try:
        eval(api_functions['type'])
        ctx_active_object = True
    except:
        ctx_active_object = False
    return ctx_active_object 

def OpenUpdateHistory(self,  context): 
    if self.history_EP != 'None' and self.history_EP != None:     
        search.FilterHistory(default_paths,  active_configuration, api_functions, active_languages,  self.history_EP)

def OpenSearch(self,  context): 
    advanced_search_properties = \
        {
            'name': self.name_BP, 
            'keywords': self.search_SP, 
            'description': self.description_BP, 
            'creator': self.creator_BP, 
            'category': self.category_BP, 
            'weblink': self.weblink_BP, 
            'email': self.email_BP, 
        }
    try:
        search.FilterSearch(default_paths,  active_configuration, api_functions, active_languages,  advanced_search_properties)
    except:
        error = active_languages['menu_error_error050'] % self.search_SP
        misc.LogAndPrintError((error,  error))

class BeforeRemoveMaterial(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_before_rem"
    bl_label = space_access_name + active_languages['bl_id_name_remove']      

    ctx = eval(api_functions['props'])
    type = ctx.EnumProperty(name='remove',  items=informations.InformationsEnumItems(default_paths['database']))

    def invoke(self, context, event):
        wm = eval(api_functions['invoke_search_popup'].replace("#1#", "self"))
        return {'PASS_THROUGH'}

    def execute(self, context):
        ops_object = eval(api_functions['ops_object'])
        eval(api_functions['utils_unregister_class'].replace("#1#", "RemoveMaterial"))
        eval(api_functions['utils_register_class'].replace("#1#", "RemoveMaterial"))
        infos = informations.InformationsSelectedItem(default_paths['database'],  self.type)
        if infos == None: 
            path = os.path.join(bookmarks_folder_path,  '.tempory')
            paths = (bookmarks_folder_path,  path)
            for e in paths:
                if os.path.exists(e) :
                    files = os.listdir(e)
                    for f in files: 
                        if not os.path.isdir(f) and self.type in f:
                            ops_object.shadertoolsng_remm('INVOKE_DEFAULT',  inf_num_SP=self.type,  inf_name_SP=f.rstrip("_(%s).jpg" % self.type))
                            break
        else:
            ops_object.shadertoolsng_remm('INVOKE_DEFAULT',  inf_num_SP=self.type,  inf_name_SP=infos[1].replace("$T_",  ""))
        return {'PASS_THROUGH'}

class RemoveMaterial(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_remm"
    bl_label = ''
    
    ctx = eval(api_functions['props'])
    #Informations properties
    inf_num_SP = ctx.StringProperty()
    inf_name_SP = ctx.StringProperty()

    def draw(self, context):
        ctx_scene = eval(api_functions['context_scene'])
        layout = self.layout
        row = layout.row(align=True)
        row.label(active_languages['menu_remove_confirmation'] + " '%s_(%s)'" % (self.inf_name_SP,  self.inf_num_SP))
        row = layout.row(align=True)
         
    def invoke(self, context, event):
        wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=370"))
        return {'RUNNING_MODAL'}
        
    def execute(self, context):
        ops_object = eval(api_functions['ops_object'])
        #materials
        condition_update = "set " + remove.MaterialRemove(self.inf_num_SP,  api_functions) + " where num_materials=%s" % self.inf_num_SP
        remove_req = request.DatabaseUpdate(default_paths['database'], "MATERIALS",  condition_update)
        #informations
        num_informations = request.DatabaseSelect(default_paths['database'], ("num_informations", ),"INFORMATIONS", "where idx_materials =%s" %self.inf_num_SP, 'one')
        condition_update = "set " + remove.InformationsRemove(self.inf_num_SP,  api_functions,  num_informations[0]) + " where idx_materials=%s" % self.inf_num_SP
        remove_req = request.DatabaseUpdate(default_paths['database'], "INFORMATIONS",  condition_update)
        #render
        num_render = request.DatabaseSelect(default_paths['database'], ("num_render", ),"RENDER", "where idx_materials =%s" %self.inf_num_SP, 'one')
        condition_update = "set " + remove.RenderRemove(self.inf_num_SP,  api_functions,  num_render[0]) + " where idx_materials=%s" % self.inf_num_SP
        remove_req = request.DatabaseUpdate(default_paths['database'], "RENDER",  condition_update)
        #textures
        all_textures = request.DatabaseSelect(default_paths['database'], ("num_textures", ),"TEXTURES", "where idx_materials =%s" %self.inf_num_SP, 'all')  
        for t in all_textures:
            condition_update = "set " + remove.TexturesRemove(self.inf_num_SP,  api_functions, default_paths,  t) + " where num_textures=%s" % t[0]
            remove_req = request.DatabaseUpdate(default_paths['database'], "TEXTURES",  condition_update)
        #diffuse ramps
        diffuse_ramps = request.DatabaseSelect(default_paths['database'], ("num_diffuse_ramps", ),"DIFFUSE_RAMPS", "where idx_materials =%s" %self.inf_num_SP, 'all')  
        for r in diffuse_ramps:
            condition_update = "set " + remove.RampsRemove(self.inf_num_SP,  api_functions, default_paths,  r,  'diffuse') + " where num_diffuse_ramps=%s" % r[0]
            remove_req = request.DatabaseUpdate(default_paths['database'], "DIFFUSE_RAMPS",  condition_update)
        #specular ramps
        specular_ramps = request.DatabaseSelect(default_paths['database'], ("num_specular_ramps", ),"SPECULAR_RAMPS", "where idx_materials =%s" %self.inf_num_SP, 'all')  
        for r in specular_ramps:
            condition_update = "set " + remove.RampsRemove(self.inf_num_SP,  api_functions, default_paths,  r,  'specular') + " where num_specular_ramps=%s" % r[0]
            remove_req = request.DatabaseUpdate(default_paths['database'], "SPECULAR_RAMPS",  condition_update)
        #color ramps
        color_ramps = request.DatabaseSelect(default_paths['database'], ("num_color_ramps", ),"COLOR_RAMPS", "where idx_materials =%s" %self.inf_num_SP, 'all')  
        for r in color_ramps:
            condition_update = "set " + remove.RampsRemove(self.inf_num_SP,  api_functions, default_paths,  r,  'color') + " where num_color_ramps=%s" % r[0]
            remove_req = request.DatabaseUpdate(default_paths['database'], "COLOR_RAMPS",  condition_update)
        #point density ramps
        point_ramps = request.DatabaseSelect(default_paths['database'], ("num_point_density_ramps", ),"POINTDENSITY_RAMPS", "where idx_materials =%s" %self.inf_num_SP, 'all')  
        for r in point_ramps:
            condition_update = "set " + remove.RampsRemove(self.inf_num_SP,  api_functions, default_paths,  r,  'point_density_color') + " where num_point_density_ramps=%s" % r[0]
            remove_req = request.DatabaseUpdate(default_paths['database'], "POINTDENSITY_RAMPS",  condition_update)

        rem_thumbnail = os.path.join(bookmarks_folder_path,  "%s_(%s).jpg" % (self.inf_name_SP,  self.inf_num_SP))
        rem_thumbnail_2 = os.path.join(bookmarks_folder_path,  '.tempory', "%s_(%s).jpg" % (self.inf_name_SP,  self.inf_num_SP))
        try:
            misc.Clear(rem_thumbnail , 'files', 'one', active_languages)
            misc.Clear(rem_thumbnail_2 , 'files', 'one', active_languages)
        except: pass
        BeforeRemoveMaterial.type[1]['items'] = informations.InformationsEnumItems(default_paths['database'])
        eval(api_functions['utils_unregister_class'].replace("#1#", "BeforeRemoveMaterial"))
        eval(api_functions['utils_register_class'].replace("#1#", "BeforeRemoveMaterial"))
        ops_object.shadertoolsng_restore('EXEC_DEFAULT')
        return {'FINISHED'}   

class ExportImportDatabase(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_iodatabase"
    bl_label = space_access_name + active_languages['bl_id_name_export_import']

    ctx = eval(api_functions['props'])
    filename_ext = ".bldb"
    filter_glob = ctx.StringProperty(default="*.bldb;*.BLDB", options={'HIDDEN'})
    filename = ctx.StringProperty(subtype="FILENAME")
    filepath = ctx.StringProperty(subtype="FILE_PATH")    
    import_BP = ctx.BoolProperty(name=active_languages['menu_tools_io_database_import'], default=0)
    export_BP = ctx.BoolProperty(name=active_languages['menu_tools_io_database_export'], default=1)

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        if not database_stuff:
            row.label(active_languages['menu_tools_io_database_title'] + ':', icon="HELP")
            row = layout.row(align=True)
            row.prop(self, "export_BP")
            row = layout.row(align=True)
            row.prop(self, "import_BP")
            row = layout.row(align=True)
        else:
            row.label(active_languages['menu_error_error040'], icon='RADIO')
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error041'])
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error042'])

    def invoke(self, context, event):
        if not database_stuff: 
           wm = eval(api_functions['fileselect_add'].replace("#1#", "self"))
        else: 
             wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self"))
        return {'RUNNING_MODAL'} 

    def execute(self, context):
        global database_stuff
        if not database_stuff: 
            new_path = self.filepath.replace(".",  "_") + ".bldb"
            new_name = self.filename.replace(".",  "_") + ".bldb"
            if self.export_BP:
                try:
                    misc.Clear(new_path, 'files', 'one', active_languages)
                    shutil.copy2(default_paths['database'],  new_path)
                    error = active_languages['menu_error_error055'] % new_name
                    misc.LogAndPrintError((error,  error))
                except:
                    error = active_languages['menu_error_error056'] % new_name
                    misc.LogAndPrintError((error,  error))

            if self.import_BP:
                try:
                    misc.SaveDatabase(default_paths['database'],  default_paths['save'],  default_paths['bin'])
                    shutil.copy2(self.filepath,  default_paths['database'])
                    error = active_languages['menu_error_error057'] % new_name
                    misc.LogAndPrintError((error,  error))
                except:
                    error = active_languages['menu_error_error058'] % new_name
                    misc.LogAndPrintError((error,  error))
        return {'FINISHED'}   

class Cleanup(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_cleanup"
    bl_label = space_access_name + active_languages['bl_id_name_tools_cleanup']
    global  database_stuff

    ctx = eval(api_functions['props'])
    temp_BP = ctx.BoolProperty(name=active_languages['menu_tools_cleanup_temp'], default=0)
    zip_BP = ctx.BoolProperty(name=active_languages['menu_tools_cleanup_zip'], default=0)
    error_BP = ctx.BoolProperty(name=active_languages['menu_tools_cleanup_logs'], default=0)
    autosave_BP = ctx.BoolProperty(name=active_languages['menu_tools_cleanup_autosave'], default=0)
    migrate_BP = ctx.BoolProperty(name=active_languages['menu_tools_cleanup_migrate'], default=0)
    pycache_BP = ctx.BoolProperty(name=active_languages['menu_tools_cleanup_pycache'], default=0)
    materials_BP = ctx.BoolProperty(name=active_languages['menu_tools_cleanup_materials_folder'], default=0)

    def invoke(self, context, event):
        if database_stuff: wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=500"))
        else: wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=400"))
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        if database_stuff: 
            row.label(active_languages['menu_error_error040'], icon='RADIO')
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error041'])
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error042'])
        else:
            row.label(active_languages['menu_tools_cleanup_title'] +':')
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error054'], icon="RADIO")
            row = layout.row(align=True)
            row.prop(self, "temp_BP")
            row.prop(self, "zip_BP")
            row = layout.row(align=True)
            row.prop(self, "error_BP")
            row.prop(self, "autosave_BP")
            row = layout.row(align=True)
            row.prop(self, "migrate_BP")
            row.prop(self, "materials_BP")
            row = layout.row(align=True)
            row.prop(self, "pycache_BP")
            row = layout.row(align=True)
            
    def execute(self, context):
        global update
        if not database_stuff: 
            choices = {"temp":self.temp_BP,  "zip":self.zip_BP, "error":self.error_BP, "autosave":self.autosave_BP, 
                           "migrate":self.migrate_BP, "pycache":self.pycache_BP, "materials":self.materials_BP}
            try:
                lauch_progress_bar = threading.Thread(None, cleanup.Selected, "Cleanup", (default_paths,  active_configuration, api_functions, active_languages, choices), {})
                lauch_progress_bar.start()
                update = True
            except:pass
        return {'PASS_THROUGH'}

class OpenAddOnFolder(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_openaddon"
    bl_label = space_access_name + active_languages['bl_id_name_open_addon']

    def execute(self, context):
        open.AddonFolder(default_paths,  active_configuration, api_functions, active_languages)
        return {'FINISHED'}

def UpdateProgressBar(self,  context): return None
def LoadingMigrateProgressBar(path):
    global database_stuff, progress_bar
    database_stuff = True
    progress_bar = True
    ctx_scene = eval(api_functions['context_scene'])
    number_max = request.DatabaseCount(path, "Mat_Index", "MATERIALS", "", 'one')
    version_values = request.DatabaseSelect(path, keys.OldVersionKeys(), "VERSION", "", 'one')
    errors_list = ("*"*78,  "*" + " "*22 + "Shader Tools Next Gen - Migrate" + " "*23 + "*", "Database version : %s" %version_values[2], )
    error_val = (0,  1,  0,  2)
    for v in error_val: misc.LogAndPrintError((errors_list[v], errors_list[v]))
    misc.SaveDatabase(default_paths['database'],  default_paths['save'],  default_paths['bin'])
 
    for v in range(2, number_max[0]+1):
        ctx_scene.shadertoolsng_utils_bar = misc.CrossProduct(v+1, number_max[0]+1)
        err = active_languages['menu_error_error037'] % str(v)
        print("\n%s" % err)
        misc.LogError("*"*3, 0)
        misc.LogError(err, 0)
        migrate.MigrateV1V2(path, api_functions, active_languages, active_configuration, default_paths, v)
        open.CreateThumbnails(default_paths,  active_configuration, api_functions, active_languages, False)
        misc.LogError("*"*3 +"\n", 0)
    database_stuff = False
    progress_bar = False

class RestoreFilters(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_restore"
    bl_label = ''

    def execute(self, context):
        database_folder = os.path.join(default_paths['app'],  active_languages['menu_bookmarks_name'])
        tempory_folder = os.path.join(database_folder,  ".tempory")
        search.MoveAllInsideFolder(active_configuration, api_functions, active_languages, tempory_folder,  database_folder)
        exec(api_functions['ops_file_refresh'])
        return {'FINISHED'}

class Errors(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_errors"
    bl_label = space_access_name + active_languages['bl_id_name_logs']

    def execute(self, context):
        global default_paths, active_configuration, api_functions
        log.OpenLog(default_paths['app'], active_configuration, api_functions)
        return {'FINISHED'}

class UpdateWarning(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_warning"
    bl_label = " "

    def execute(self, context):
        return {'FINISHED'}

class BeforeOpen(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_before"
    bl_label = ''

    def draw(self, context):
        global  database_stuff
        if database_stuff:
            layout = self.layout
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error040'], icon='RADIO')
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error041'])
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error042'])

    def invoke(self, context, event):
        global  database_stuff,  active_history
        if database_stuff : 
            wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=500"))
            return {'RUNNING_MODAL'}
        else: 
            ops_object = eval(api_functions['ops_object'])
            Open.history_EP[1]['items'] = active_history
            BeforeRemoveMaterial.type[1]['items'] = informations.InformationsEnumItems(default_paths['database'])
            eval(api_functions['utils_unregister_class'].replace("#1#", "BeforeRemoveMaterial"))
            eval(api_functions['utils_register_class'].replace("#1#", "BeforeRemoveMaterial"))
            eval(api_functions['utils_unregister_class'].replace("#1#", "Open"))
            eval(api_functions['utils_register_class'].replace("#1#", "Open"))

            database_folder = os.path.join(default_paths['app'],  active_languages['menu_bookmarks_name'])
            tempory_folder = os.path.join(database_folder,  ".tempory")
            search.MoveAllInsideFolder(active_configuration, api_functions, active_languages, tempory_folder,  database_folder)
            ops_object.shadertoolsng_open('INVOKE_DEFAULT')
            return {'FINISHED'}

    def execute(self, context): return {'FINISHED'}   

class InformationsWeblink(eval(api_functions['types_operator'])): 
    bl_idname = "object.shadertoolsng_weblink"
    bl_label = ''    
    
    def execute(self, context):
        global  inf_current_weblink
        try:
            if  inf_current_weblink:
                webbrowser.open_new( inf_current_weblink)
                inf_current_weblink = False
        except:pass
        return {'FINISHED'}   

class BeforeInformations(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_before_inf"
    bl_label = space_access_name + active_languages['bl_id_name_search_infos']      

    ctx = eval(api_functions['props'])
    type = ctx.EnumProperty(name='info',  items=informations.InformationsEnumItems(default_paths['database']))

    def invoke(self, context, event):
        wm = eval(api_functions['invoke_search_popup'].replace("#1#", "self"))
        return {'PASS_THROUGH'}

    def execute(self, context):
        global inf_current_weblink
        ops_object = eval(api_functions['ops_object'])
        eval(api_functions['utils_unregister_class'].replace("#1#", "Informations"))
        eval(api_functions['utils_register_class'].replace("#1#", "Informations"))
        infos = informations.InformationsSelectedItem(default_paths['database'],  self.type)
        if infos == None: 
            ops_object.shadertoolsng_infos('INVOKE_DEFAULT',  inf_name_SP='No informations',  inf_creator_SP='No informations',  inf_description_SP='No informations', 
                                                                inf_category_SP='No informations',  inf_weblink_SP='No informations',  inf_email_SP='No informations')      
        else:
            inf_current_weblink = infos[5]
            ops_object.shadertoolsng_infos('INVOKE_DEFAULT',  inf_name_SP=infos[1].replace("$T_",  ""),  inf_creator_SP=infos[3],  inf_description_SP=infos[2], 
                                                                inf_category_SP=infos[4],  inf_weblink_SP=infos[5],  inf_email_SP=infos[6])      
        return {'PASS_THROUGH'}

class Informations(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_infos"
    bl_label = ''
    
    ctx = eval(api_functions['props'])
    #Informations properties
    inf_name_SP = ctx.StringProperty()
    inf_description_SP = ctx.StringProperty(name=active_languages['menu_information_description'])
    inf_creator_SP = ctx.StringProperty()
    inf_category_SP = ctx.StringProperty(name=active_languages['menu_information_category'])
    inf_weblink_SP = ctx.StringProperty()
    inf_email_SP = ctx.StringProperty(name=active_languages['menu_information_email'])

    def draw(self, context):
        global inf_current_self,  inf_current_context
        inf_current_self = self
        inf_current_context = context
        ctx_scene = eval(api_functions['context_scene'])
        layout = self.layout
        row = layout.row(align=True)
        row.label(active_languages['menu_information_label01'])
        row = layout.row(align=True)
        row.label(active_languages['menu_information_label02'] + " :")                        
        row.label(self.inf_name_SP)                        
        row = layout.row(align=True)
        row.label(active_languages['menu_information_creator'] + " :") 
        row.label(self.inf_creator_SP)            
        row = layout.row(align=True)
        row.label(active_languages['menu_information_category'] + " :") 
        row.label(self.inf_category_SP)
        row = layout.row(align=True)
        row.label(active_languages['menu_information_email'] + " :") 
        row.label(self.inf_email_SP)
        row = layout.row(align=True)
        row.prop(self, "inf_description_SP")
        row = layout.row(align=True)
        row.operator("object.shadertoolsng_weblink",  text=active_languages['menu_information_weblink'])            
        row = layout.row(align=True)
         
    def invoke(self, context, event):
        wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=400"))
        return {'RUNNING_MODAL'}
        
    def execute(self, context): 
        return {'FINISHED'}   

class Open(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_open"
    bl_label = space_access_name + active_languages['bl_id_name_open']  

    ctx = eval(api_functions['props'])
    types_scene = eval(api_functions['types_scene'])
    msg = "%s %s" % (active_languages['menu_search_label02'] ,  active_languages['menu_search_label03'])

    filename_ext = ".jpg"
    filename = ctx.StringProperty(subtype="FILENAME")
    #Search properties
    name_BP = ctx.BoolProperty(name=active_languages['menu_search_name'], default=1)
    history_EP = ctx.EnumProperty(name=active_languages['menu_history_label01'],items=(active_history),  update=OpenUpdateHistory)
    search_SP = ctx.StringProperty(name=active_languages['menu_search_label01'],  update=OpenSearch,  description=msg)
    description_BP = ctx.BoolProperty(name=active_languages['menu_search_description'], default=0)
    creator_BP = ctx.BoolProperty(name=active_languages['menu_search_creator'], default=0)
    category_BP = ctx.BoolProperty(name=active_languages['menu_search_category'], default=0)
    weblink_BP = ctx.BoolProperty(name=active_languages['menu_search_weblink'], default=0)
    email_BP = ctx.BoolProperty(name=active_languages['menu_search_email'], default=0)
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(active_languages['menu_search_title'])
        row = layout.row(align=True)
        row.prop(self, "search_SP") 
        row = layout.row(align=True)
        row.label(active_languages['menu_search_label04'])
        row = layout.row(align=True)
        row.prop(self, "name_BP")            
        row.prop(self, "description_BP")            
        row = layout.row(align=True)
        row.prop(self, "creator_BP")
        row.prop(self, "category_BP")                        
        row = layout.row(align=True)
        row.prop(self, "weblink_BP")            
        row.prop(self, "email_BP")            
        row = layout.row(align=True)
        row.label(" ")
        row = layout.row(align=True)
        row.label(active_languages['menu_history_title'])
        row = layout.row(align=True)
        row.prop(self, "history_EP")            
        row = layout.row(align=True)
        row.label(" ")
        row = layout.row(align=True)
        row.operator("object.shadertoolsng_restore", text=active_languages['menu_open_restore'], icon='FILE_REFRESH')
        row = layout.row(align=True)
        row.operator("object.shadertoolsng_before_inf", text=active_languages['menu_information_label01'], icon='INFO')
        row = layout.row(align=True)
        row.operator("object.shadertoolsng_before_rem", text=active_languages['buttons_remove'], icon='X')
        row = layout.row(align=True)
        row.label(" ")
            
    def invoke(self, context, event):
        eval(api_functions['utils_unregister_class'].replace("#1#", "BeforeInformations"))
        eval(api_functions['utils_register_class'].replace("#1#", "BeforeInformations"))
        wm = eval(api_functions['fileselect_add'].replace("#1#", "self"))
        return {'RUNNING_MODAL'}
        
    def execute(self, context):
        global active_history
        ctx_scene = eval(api_functions['context_scene'])
        ops_object = eval(api_functions['ops_object'])
        ctx = eval(api_functions['props'])
        ctx_scene.shadertoolsng_utils_bar = 0
        step_number = 4
        open.ImportMaterialInApp(default_paths,  active_configuration, api_functions, active_languages, self.filename,  step_number)
        history.UpdateHistory(default_paths,  active_configuration, api_functions, active_languages,  self.filename,  active_history)
        active_history = history.CurrentHistory(default_paths,  active_configuration, api_functions, active_languages)
        return {'FINISHED'}

def SaveInsideDatabase(save_request):
    global database_stuff, progress_bar
    database_stuff = True
    progress_bar = True
    ctx_scene = eval(api_functions['context_scene'])
    v = 0
    for e in save_request:
        if v in range(0, 3): request.DatabaseInsert(default_paths['database'], e[1], '', '',  False,  'force')
        else: 
            for r in e[1]:
                if type(r[1]).__name__ == 'str': request.DatabaseInsert(default_paths['database'], r[1], '', '',  False,  'force')
                else: 
                    for p in r[1]: request.DatabaseInsert(default_paths['database'], p[1], '', '',  False,  'force')
        try:ctx_scene.shadertoolsng_utils_bar = misc.CrossProduct(v+1, save_request.__len__()+1)
        except:pass
        v = v + 1
    open.CreateThumbnails(default_paths,  active_configuration, api_functions, active_languages, False, )
    ctx_scene.shadertoolsng_utils_bar = 100
    database_stuff = False
    progress_bar = False
            

class Save(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_save"
    bl_label = space_access_name + active_languages['bl_id_name_save']    

    global  database_stuff
    ctx = eval(api_functions['props'])
    name_SP = ctx.StringProperty(name=active_languages['menu_save_material_title'], default=active_configuration['material_name'])
    creator_SP = ctx.StringProperty(name=active_languages['menu_save_creator_name_title'], default=active_configuration['author'])
    weblink_SP = ctx.StringProperty(name=active_languages['menu_save_web_link_title'], default=active_configuration['web_link'])
    email_SP = ctx.StringProperty(name=active_languages['menu_save_email_title'], default=active_configuration['email_creator'])
    key_words_SP = ctx.StringProperty(name=active_languages['menu_save_key_words_title'], default=active_configuration['key_words'])
    description_SP = ctx.StringProperty(name=active_languages['menu_save_description_title'], default=active_configuration['description'])    
    category_EP = ctx.EnumProperty(name=active_languages['menu_configuration_category'],items=(active_categories),default=active_configuration['category'])
   
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        if database_stuff: 
            row.label(active_languages['menu_error_error040'], icon='RADIO')
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error041'])
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error042'])
        else: 
            if ctx_active_object():
                row.label(active_languages['menu_save_title'] + ":",  icon='INFO')
                row = layout.row(align=True)
                row.prop(self, "name_SP")  
                row = layout.row(align=True)
                row.prop(self, "creator_SP")    
                row = layout.row(align=True)
                row.prop(self, "weblink_SP")    
                row = layout.row(align=True)
                row.prop(self, "email_SP")    
                row = layout.row(align=True)
                row.prop(self, "description_SP")    
                row = layout.row(align=True)
                row.prop(self, "key_words_SP")    
                row = layout.row(align=True)
                row.prop(self, "category_EP")    
                row = layout.row(align=True)
            else:
                row.label(active_languages['menu_error_error059'], icon='RADIO')
 
    def invoke(self, context, event):
        if not database_stuff and ctx_active_object(): wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=500"))
        else: wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=500"))
        return {'RUNNING_MODAL'} 
    
    def execute(self, context):
        global database_stuff, default_paths, active_configuration, api_functions
        if not database_stuff:
            ops_object = eval(api_functions['ops_object'])
            num_material = request.DatabaseMax(default_paths['database'], "num_materials", "MATERIALS", "", 'one')[0] + 1
            num_information = request.DatabaseMax(default_paths['database'], "num_informations", "INFORMATIONS", "", 'one')[0] + 1
            num_render = request.DatabaseMax(default_paths['database'], "num_render", "RENDER", "", 'one')[0] + 1
            num_texture = request.DatabaseMax(default_paths['database'], "num_textures", "TEXTURES", "", 'one')[0] + 1
            num_diffuse_ramp = request.DatabaseMax(default_paths['database'], "num_diffuse_ramps", "DIFFUSE_RAMPS", "", 'one')[0] + 1
            num_specular_ramp = request.DatabaseMax(default_paths['database'], "num_specular_ramps", "SPECULAR_RAMPS", "", 'one')[0] + 1
            num_color_ramp = request.DatabaseMax(default_paths['database'], "num_color_ramps", "COLOR_RAMPS", "", 'one')[0] + 1
            num_pointdensity_ramp = request.DatabaseMax(default_paths['database'], "num_point_density_ramps", "POINTDENSITY_RAMPS", "", 'one')[0] + 1

            request_dict = \
                    {
                     "informations":True,  "material":True,  "diffuse_ramps":True,  "specular_ramps":True, 
                     "textures":True,  "color_ramps":True,  "pointdensity_ramps":True,  "render":True, 
                     }
            material_exceptions = \
                (
                 self.name_SP,  self.creator_SP,  self.weblink_SP, self.email_SP, 
                 self.description_SP, self.key_words_SP, self.category_EP,  
                )
            material_input = []
            for m in material_exceptions: material_input.append(keys.InputExceptionsKeys(m))    
            material_dict = \
                    {
                     "material_name": material_input[0], "name": "$T_%s" % material_input[0], "creator":material_input[1],
                     "weblink":material_input[2],"email":material_input[3],"description":material_input[4],
                     "key_words":material_input[5], "category":material_input[6],
                     "paths":default_paths, "idx_materials":num_material, "num_informations":num_information, "num_render":num_render, 
                     "idx_textures":num_texture, "idx_diffuse_ramp":num_diffuse_ramp, "idx_specular_ramp":num_specular_ramp, 
                     "filename":material_input[0], "filepath":os.path.join(default_paths['temp'],  'tempory_name.jpg'),
                     "type":eval(api_functions['type']),  "preview_render_type":eval(api_functions['preview_render_type']),
                     "num_materials":num_material, "num_textures":num_texture, "idx_color_ramp":num_color_ramp, 
                     "idx_point_density_color_ramp":num_pointdensity_ramp, "use_textures":1, "texture_use_alpha":0,
                     "temp":default_paths['temp'], 
                    }
            #Test all requests before commit:
            save_request = []
            save_request.append(save.InformationsSave(material_dict, api_functions, active_languages, active_configuration, True))
            save_request.append(save.RenderSave(material_dict, api_functions, active_languages, active_configuration, True, default_paths))
            save_request.append(save.MaterialSave(material_dict, api_functions, active_languages, active_configuration, True))
            if eval(api_functions['use_diffuse_ramp']):
                save_request.append(save.RampsSave(material_dict, api_functions, active_languages, active_configuration, 'diffuse',  True,  ''))
            if eval(api_functions['use_specular_ramp']):
                save_request.append(save.RampsSave(material_dict, api_functions, active_languages, active_configuration, 'specular',  True,  ''))
            save_request.append(save.TexturesSave(material_dict, api_functions, active_languages, active_configuration, True))

            request_progress_bar = threading.Thread(None, SaveInsideDatabase, "Save inside database", (save_request, ), {})
            request_progress_bar.start()
        return {'PASS_THROUGH'}   

class Export(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_export"
    bl_label = space_access_name + active_languages['bl_id_name_export']    

    global default_paths
    ctx = eval(api_functions['props'])
    filename_ext = ".blex"
    filter_glob = ctx.StringProperty(default="*.blex;*.BLEX", options={'HIDDEN'})
    filename = ctx.StringProperty(subtype="FILENAME")
    filepath = ctx.StringProperty(subtype="FILE_PATH")    

    creator_SP = ctx.StringProperty(name=active_languages['menu_configuration_creator_name'], default=active_configuration['author'])
    take_preview_BP = ctx.BoolProperty(name=active_languages['take_preview'], default=int(active_configuration['take_preview']))
    weblink_SP = ctx.StringProperty(name=active_languages['menu_configuration_web_link'], default=active_configuration['web_link'])
    email_SP = ctx.StringProperty(name=active_languages['menu_configuration_email'], default=active_configuration['email_creator'])
    key_words_SP = ctx.StringProperty(name=active_languages['menu_configuration_key_words'], default=active_configuration['key_words'])
    description_SP = ctx.StringProperty(name=active_languages['menu_configuration_description'], default=active_configuration['description'])

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        if ctx_active_object():
            row.label(active_languages['menu_configuration_material_name'] + ":")
            row.label(eval(api_functions['material_name']))
            row = layout.row(align=True)
            row.prop(self, "take_preview_BP")    
            row = layout.row(align=True)
            row.prop(self, "creator_SP")    
            row = layout.row(align=True)
            row.prop(self, "weblink_SP")    
            row = layout.row(align=True)
            row.prop(self, "email_SP")    
            row = layout.row(align=True)
            row.prop(self, "description_SP")    
            row = layout.row(align=True)
            row.prop(self, "key_words_SP")    
        else:
            row.label(active_languages['menu_error_error002'], icon='RADIO')

    def invoke(self, context, event):
        if ctx_active_object(): wm = eval(api_functions['fileselect_add'].replace("#1#", "self"))
        else: wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=500"))
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if ctx_active_object():
            global default_paths, active_configuration, api_functions,  active_languages
            material_exceptions = \
                (
                 eval(api_functions['material_name']),  self.creator_SP,  self.weblink_SP, 
                 self.email_SP, self.description_SP, self.key_words_SP,  
                )
            material_input = []
            for m in material_exceptions: material_input.append(keys.InputExceptionsKeys(m))    
            material_dict = \
                    {
                     "filepath":self.filepath.replace(".",  "_"), "filename":self.filename.replace(".",  "_"), "app_path":default_paths['app'],
                     "material_name":material_input[0], "creator":material_input[1],
                     "weblink":material_input[2],"email":material_input[3],"description":material_input[4],
                     "key_words":material_input[5], "take_preview":self.take_preview_BP,
                     "temp":default_paths['temp'],  "zip":default_paths['zip'],
                    }
            misc.Clear(os.path.join(material_dict['temp'], material_dict['material_name']), 'files', 'all', active_languages)
            exporter.MaterialExport(material_dict, api_functions, active_languages)
            exporter.MaterialRampsExport(material_dict, api_functions, 'diffuse', active_languages)
            exporter.MaterialRampsExport(material_dict, api_functions, 'specular', active_languages)
            exporter.TextureExport(material_dict, api_functions, active_languages)
            try:
                zip_file_path = zip.Zip(material_dict, api_functions, active_languages)
                if material_dict['filepath'].find(".blex") < 0:
                    material_dict['filepath'] = material_dict['filepath'] + ".blex"
                shutil.copy2(zip_file_path, material_dict['filepath'])
                print(active_languages['menu_error_error027'])
                misc.LogError(active_languages['menu_error_error027'], False)
            except:
                print(active_languages['menu_error_error028'])
                misc.LogError(active_languages['menu_error_error028'], False)
            try:
                misc.Clear(default_paths['zip'], 'all', '', active_languages)
                misc.Clear(default_paths['temp'], 'all', '', active_languages)
            except: pass
            if self.take_preview_BP:
                try: 
                    render.PreviewRenderInternal(default_paths, api_functions, active_configuration,  active_languages, material_dict,  '')
                    print(active_languages['menu_error_error023'])
                    misc.LogError(active_languages['menu_error_error023'], False)
                except:
                    print(active_languages['menu_error_error024'])
                    misc.LogError(active_languages['menu_error_error024'], False)
        else:
            eval(api_functions['utils_unregister_class'].replace("#1#", "Export"))
            eval(api_functions['utils_register_class'].replace("#1#", "Export"))
        return {'FINISHED'}   

class Import(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_import"
    bl_label = space_access_name + active_languages['bl_id_name_import']    

    global default_paths
    ctx = eval(api_functions['props'])
    filename_ext = ".blex"
    filter_glob = ctx.StringProperty(default="*.blex;*.BLEX", options={'HIDDEN'})
    filename = ctx.StringProperty(subtype="FILENAME")
    filepath = ctx.StringProperty(subtype="FILE_PATH")    

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        if not eval(api_functions['blend_save']):
            row.label(active_languages['menu_error_error050'], icon="RADIO")
        else:
            row.label(active_languages['menu_import_label001'], icon="HELP")
            row = layout.row(align=True)
            row.label(eval(active_languages['menu_import_label002']))

    def invoke(self, context, event):
        if not eval(api_functions['blend_save']): wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self"))
        else: wm = eval(api_functions['fileselect_add'].replace("#1#", "self"))
        return {'RUNNING_MODAL'}

    def execute(self, context):
        importer.BlexImport(self.filepath, api_functions, active_languages, active_configuration,default_paths)
        return {'FINISHED'}   

class New(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_new"
    bl_label = space_access_name + active_languages['bl_id_name_create']    
    global  database_stuff

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        if database_stuff: 
            row.label(active_languages['menu_error_error040'], icon='RADIO')
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error041'])
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error042'])

    def invoke(self, context, event):
        if database_stuff: 
            wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=500"))
            return {'RUNNING_MODAL'} 
        else:
            new.CreateNew(default_paths['app'], active_configuration, api_functions, active_languages) 
            return {'PASS_THROUGH'} 

    def execute(self, context): return {'PASS_THROUGH'}   

def ConfigurationUpdateDefaultConfig(self,  context):
    global default_paths,  active_configuration,  configurations_config,  conf_current_idx
    try:
        request.DatabaseUpdate(default_paths['configs_database'], 'CONFIGURATION', 'set default_config=0 where default_config=1')
        request.DatabaseUpdate(default_paths['configs_database'], 'CONFIGURATION', 'set default_config=1 where num_configuration=%s' % str(conf_current_idx))
        configurations_config = environment.ConfigurationsDatas(default_paths['configs_database'], False)
        active_configuration = environment.ActiveConfigurations(configurations_config)
        default_paths = environment.ConvertDefaultPaths(default_paths,  active_configuration)
        lauch_progress_bar = threading.Thread(None, open.CreateThumbnails, "Create_thumbnails", (default_paths,  active_configuration, api_functions, active_languages, False, ), {})
        lauch_progress_bar.start()
    except:
        error = active_languages['menu_error_error051']
        misc.LogAndPrintError((error,  error))
        pass
    return None
    
class Configuration(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_configuration"
    bl_label = space_access_name + active_languages['bl_id_name_config']    
    
    ctx = eval(api_functions['props'])
    conf_choice_EP = ctx.EnumProperty(name=active_languages['menu_configuration_select_title'],items=(names_config))
    conf_language_EP = ctx.EnumProperty(name=active_languages['menu_configuration_langage_choice'],items=(names_languages),default=active_configuration['language'])
    conf_options_EP = ctx.EnumProperty(name=active_languages['menu_configuration_options'],items=(options_actions),default=active_configuration['option'],)
    category_EP = ctx.EnumProperty(name=active_languages['menu_configuration_category'],items=(active_categories),default=active_configuration['category'])
    conf_name_SP = ctx.StringProperty(name=active_languages['menu_configuration_name'], default=active_configuration['name'])
    conf_current_name = active_configuration['name']
    conf_default_BP = ctx.BoolProperty(name="", default=active_configuration['default_config'],  update=ConfigurationUpdateDefaultConfig)
    mat_name_SP = ctx.StringProperty(name=active_languages['menu_configuration_material_name'], default=active_configuration['material_name'])
    key_words_SP = ctx.StringProperty(name=active_languages['menu_configuration_key_words'], default=active_configuration['key_words'])
    description_SP = ctx.StringProperty(name=active_languages['menu_configuration_description'], default=active_configuration['description'])
    creator_SP = ctx.StringProperty(name=active_languages['menu_configuration_creator_name'], default=active_configuration['author'])
    weblink_SP = ctx.StringProperty(name=active_languages['menu_configuration_web_link'], default=active_configuration['web_link'])
    email_SP = ctx.StringProperty(name=active_languages['menu_configuration_email'], default=active_configuration['email_creator'])
    conf_res_x_IP = ctx.IntProperty(name=active_languages['menu_configuration_resolution_x'], min=active_configuration['resolution_min'], \
                                    max=active_configuration['resolution_max'], default=active_configuration['resolution_default_x'])
    conf_res_y_IP = ctx.IntProperty(name=active_languages['menu_configuration_resolution_y'], min=active_configuration['resolution_min'], \
                                    max=active_configuration['resolution_max'], default=active_configuration['resolution_default_y'])
    take_preview_BP = ctx.BoolProperty(name="", default=int(active_configuration['take_preview']))
    database_SP = ctx.StringProperty(name=active_languages['menu_configuration_base_path'], default=misc.ConvertMarkOut(active_configuration['database_path'], default_paths['app']))
    auto_save_IP = ctx.IntProperty(name="", min=1, max=50, default=active_configuration['auto_save'])
    file_browser_SP= ctx.StringProperty(name=active_languages['menu_configuration_file_browser'], default="nautilus")

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_current_index'] + ":")
        row.label(conf_current_idx)
        row.label(" ")
        row = layout.row(align=True)
        row.prop(self, "conf_name_SP")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_default_config'] + ":")
        row.prop(self, "conf_default_BP")
        row.label(" ")
        row.label(" ")
        row = layout.row(align=True)
        row.prop(self, "conf_language_EP")
        row = layout.row(align=True)
        row.prop(self, "conf_options_EP")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_informations'])
        row = layout.row(align=True)
        row.prop(self, "mat_name_SP")
        row = layout.row(align=True)
        row.prop(self, "description_SP")
        row = layout.row(align=True)
        row.prop(self, "creator_SP")
        row = layout.row(align=True)
        row.prop(self, "weblink_SP")
        row = layout.row(align=True)
        row.prop(self, "email_SP")
        row = layout.row(align=True)
        row.prop(self, "category_EP")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_preview_parameters'])
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_resolution_x'] + ":")
        row.prop(self, "conf_res_x_IP")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_resolution_y'] + ":")
        row.prop(self, "conf_res_y_IP")
        row = layout.row(align=True)
        row.label(active_languages['take_preview'] + ":")
        row.prop(self, "take_preview_BP")
        row.label(" ")
        row.label(" ")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_base_parameters'])
        row = layout.row(align=True)
        row.prop(self, "database_SP")
        row = layout.row(align=True)
        row.label(active_languages['menu_configuration_auto_save_1'] )
        row.prop(self, "auto_save_IP")
        row.label(active_languages['menu_configuration_auto_save_2'] )
        if platform.system() == "Linux":
            row = layout.row(align=True)
            row.prop(self, "file_browser_SP")

    def invoke(self, context, event):
        wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self, width=520"))
        return {'RUNNING_MODAL'}

    def execute(self, context):
        global default_paths, languages_config, active_configuration, active_languages, active_categories, names_config, options_actions,\
               names_languages, space_access_name, ConfigurationSearch, conf_current_idx, update
        if self.conf_language_EP != active_configuration['language'] and self.conf_default_BP: update = True
        elif self.conf_language_EP != active_configuration['language'] : update = True
        
        configurations_config = environment.ConfigurationsDatas(default_paths['configs_database'], False)
        c = self.conf_options_EP.split("_")[-1]
        if c == "delete":
            my_new_config = \
                {"num_configuration": conf_current_idx, "default_config":misc.ConvertBoolStringToNumber(self.conf_default_BP), 
                 "name":'', "database_path":'', "author":'', "description":'',
                 "web_link":'', "material_name":'', "key_words":'', "category":'', "email_creator":'', "resolution_min":0, 
                 "resolution_default_x":0, "resolution_default_y":0, "resolution_max":0, "language":'', "error_folder":'',
                "html_folder":'', "save_folder":'', "temp_folder":'', "zip_folder":'', "workbase_file_path":'', "bin_folder":'', 
                "help_file_path":'', "img_file_path":'', "option":'', "take_preview":0,"auto_save":0, "load_number":0, 
                "file_browser": '',  "web_browser":''}
            configuration.DeleteConfiguration(default_paths['configs_database'], my_new_config, names_config, active_languages)
        else:
            my_new_config = \
                {"num_configuration": conf_current_idx, "default_config":misc.ConvertBoolStringToNumber(self.conf_default_BP), "name":self.conf_name_SP, 
                 "database_path":self.database_SP, "author":self.creator_SP, "description":self.description_SP,
                 "web_link":self.weblink_SP, "material_name":self.mat_name_SP, "key_words":self.key_words_SP,
                 "category":self.category_EP, "email_creator":self.email_SP,
                 "resolution_min":active_configuration['resolution_min'], "resolution_default_x":self.conf_res_x_IP,
                 "resolution_default_y":self.conf_res_y_IP, "resolution_max":active_configuration['resolution_max'],
                 "language":self.conf_language_EP, "error_folder":active_configuration['error_folder'],
                 "html_folder":active_configuration['html_folder'], "save_folder":active_configuration['save_folder'],
                 "temp_folder":active_configuration['temp_folder'], "zip_folder":active_configuration['zip_folder'],
                 "workbase_file_path":active_configuration['workbase_file_path'], 
                 "bin_folder":active_configuration['bin_folder'], "help_file_path":active_configuration['help_file_path'],
                 "img_file_path":active_configuration['img_file_path'], "option":'menu_configuration_option_save', "name2":self.conf_name_SP,
                 "take_preview":misc.ConvertBoolStringToNumber(self.take_preview_BP), "auto_save":self.auto_save_IP,  "load_number":0, 
                 "file_browser":self.file_browser_SP,  "web_browser":''}
            configuration.SaveConfiguration(default_paths['configs_database'], my_new_config, active_languages)

        configurations_config = environment.ConfigurationsDatas(default_paths['configs_database'], False)
        active_configuration = environment.ActiveConfigurations(configurations_config)
        names_config = environment.ConfigurationsNames(configurations_config)
        options_actions = environment.ConfigurationsOptions(active_languages)
        ConfigurationSearch.type[1]['items'] = names_config
        Configuration.conf_choice_EP[1]['items'] = names_config

        class_reg = ("ConfigurationSearch", "Export",)
        for c in class_reg:        
                eval(api_functions['utils_unregister_class'].replace("#1#", c))
                eval(api_functions['utils_register_class'].replace("#1#", c))
        default_paths = environment.ConvertDefaultPaths(default_paths,  active_configuration)
        lauch_progress_bar = threading.Thread(None, open.CreateThumbnails, "Create_thumbnails", (default_paths,  active_configuration, api_functions, active_languages, False, ), {})
        lauch_progress_bar.start()
        return {'FINISHED'}

class ConfigurationSearch(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_configuration_search"
    bl_label = ''
    
    global  database_stuff
    ctx = eval(api_functions['props'])
    type = ctx.EnumProperty(name=active_languages['menu_configuration_select_title'],items=(names_config),)
        
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(active_languages['menu_error_error040'], icon='RADIO')
        row = layout.row(align=True)
        row.label(active_languages['menu_error_error041'])
        row = layout.row(align=True)
        row.label(active_languages['menu_error_error042'])
        
    def invoke(self, context, event):
        if not database_stuff: 
            wm = eval(api_functions['invoke_search_popup'].replace("#1#", "self"))
        else: 
             wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self"))
        return {'PASS_THROUGH'}

    def execute(self, context):
        global default_paths, conf_current_name, conf_current_idx,  database_stuff
        if not database_stuff: 
            conf_current_idx = str(self.type)
            ops_object = eval(api_functions['ops_object'])
            configurations_config = environment.ConfigurationsDatas(default_paths['configs_database'], False)
            selected_configuration = configurations_config[misc.EnumPropertyItemsInverseIdx(conf_current_idx, configurations_config)]
            conf_current_name = selected_configuration['name']
            eval(api_functions['utils_unregister_class'].replace("#1#", "Configuration"))
            eval(api_functions['utils_register_class'].replace("#1#", "Configuration"))
            ops_object.shadertoolsng_configuration('INVOKE_DEFAULT', conf_choice_EP=conf_current_idx , conf_language_EP=selected_configuration['language'],  
                                 conf_options_EP=selected_configuration['option'], category_EP=selected_configuration['category'],
                                 conf_name_SP=selected_configuration['name'], conf_default_BP=selected_configuration['default_config'],
                                 mat_name_SP=selected_configuration['material_name'], key_words_SP=selected_configuration['key_words'],
                                 description_SP=selected_configuration['description'], creator_SP=selected_configuration['author'],
                                 weblink_SP=selected_configuration['web_link'], email_SP=selected_configuration['email_creator'],
                                 conf_res_x_IP=selected_configuration['resolution_default_x'], conf_res_y_IP=selected_configuration['resolution_default_y'],
                                 database_SP=misc.ConvertMarkOut(selected_configuration['database_path'], default_paths['app']),
                                 take_preview_BP=int(selected_configuration['take_preview']),  auto_save_IP=selected_configuration['auto_save'], 
                                 file_browser_SP=str(selected_configuration['file_browser']))
        return {'PASS_THROUGH'}   

class Help(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_help"
    bl_label = space_access_name + active_languages['bl_id_name_help']    

    def execute(self, context):
        help.help_me(default_paths['app'], active_languages['name_language'])
        return {'FINISHED'}   

class Credits(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_credits"
    bl_label = space_access_name + active_languages['bl_id_name_credits']    

    def draw(self, context):
        credits_keys = keys.CreditsKeys()
        layout = self.layout
        row = layout.row(align=True)
        row.label("Credits :", icon='QUESTION')
        for k in credits_keys:
            row = layout.row(align=True)
            r = credits.ShowCredits(about_config[k])
            for v in r:
                row.label(v[0])
                row.label(v[1])
                row = layout.row(align=True)

    def invoke(self, context, event):
        return eval(api_functions['invoke_popup'].replace("#1#", "self, width = 380"))

    def execute(self, context):
        return {'FINISHED'}   

class UtilsMigrate(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_utils_migrate"
    bl_label = space_access_name + active_languages['bl_id_name_utils_migrate']    

    global database_stuff,  progress_bar
    
    ctx = eval(api_functions['props'])
    filename_ext = ".sqlite"
    filter_glob = ctx.StringProperty(default="*.sqlite;*.SQLITE", options={'HIDDEN'})
    filename = ctx.StringProperty(subtype="FILENAME")
    filepath = ctx.StringProperty(subtype="FILE_PATH")   

    def draw(self, context):
        if not database_stuff:
            layout = self.layout
            row = layout.row(align=True)
            row.label(active_languages['menu_utils_migrate_help01'], icon="HELP")
            row = layout.row(align=True)
        else:
            layout = self.layout
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error040'], icon='RADIO')
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error041'])
            row = layout.row(align=True)
            row.label(active_languages['menu_error_error042'])

    def invoke(self, context, event):
        if not database_stuff: 
           wm = eval(api_functions['fileselect_add'].replace("#1#", "self"))
        else: 
             wm = eval(api_functions['invoke_props_dialog'].replace("#1#", "self"))
        return {'RUNNING_MODAL'} 

    def execute(self, context):
        global database_stuff,  progress_bar
        if not database_stuff: 
            progress_bar = True
            lauch_progress_bar = threading.Thread(None, LoadingMigrateProgressBar, None, (self.filepath,), {})
            lauch_progress_bar.start()
        return {'FINISHED'}   

def OpenSaveSwitch(self, context):
    ops_object = eval(api_functions['ops_object'])
    if self.shadertoolsng_open_save == 'buttons_open':ops_object.shadertoolsng_before('INVOKE_DEFAULT')
    else:ops_object.shadertoolsng_save('INVOKE_DEFAULT')

def ExportImportSwitch(self, context):
    ops_object = eval(api_functions['ops_object'])
    if self.shadertoolsng_export_import == 'buttons_export':ops_object.shadertoolsng_export('INVOKE_DEFAULT')
    else:ops_object.shadertoolsng_import('INVOKE_DEFAULT')

def UtilsSwitch(self, context):
    ops_object = eval(api_functions['ops_object'])
    if self.shadertoolsng_utils_enum == 'buttons_config':ops_object.shadertoolsng_configuration_search('INVOKE_DEFAULT')
    elif self.shadertoolsng_utils_enum == 'buttons_log':ops_object.shadertoolsng_errors('INVOKE_DEFAULT')
    elif self.shadertoolsng_utils_enum == 'buttons_help':ops_object.shadertoolsng_help('INVOKE_DEFAULT')
    elif self.shadertoolsng_utils_enum == 'buttons_create':ops_object.shadertoolsng_new('INVOKE_DEFAULT')
    elif self.shadertoolsng_utils_enum == 'menu_utils_migrate':ops_object.shadertoolsng_utils_migrate('INVOKE_DEFAULT')
    elif self.shadertoolsng_utils_enum == 'buttons_addon_folder_access':ops_object.shadertoolsng_openaddon('INVOKE_DEFAULT')
    elif self.shadertoolsng_utils_enum == 'buttons_tools_cleanup':ops_object.shadertoolsng_cleanup('INVOKE_DEFAULT')
    elif self.shadertoolsng_utils_enum == 'buttons_export_import':ops_object.shadertoolsng_iodatabase('INVOKE_DEFAULT')
    else:ops_object.shadertoolsng_credits('INVOKE_DEFAULT')

def SwitchButtonsList(list):
    temp = []
    for p in list: temp.append(tuple((p, active_languages[p], "")))
    return temp

def ActivePreview(type):
    elements_preview = ['Cube',  'Plane', 'Sphere',  'Monkey', ]
    elements_preview.remove(type)    
    for e in elements_preview:
       for v in ('hide_object',  'hide_render'): exec("%s = True" % api_functions[v] % e)
    for v in ('hide_object',  'hide_render'): exec("%s = False" % api_functions[v] % type)
    exec(api_functions['select_name'] % type)
    if type == 'Plane': exec("%s = 'FLAT'" % api_functions['preview_render_type'])
    else: exec("%s = '%s'" % (api_functions['preview_render_type'],  type.upper()))
    
class SuzannePreview(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_suzanne"
    bl_label = ""    
    
    def execute(self, context):
        try: ActivePreview('Monkey')
        except: pass
        return {'FINISHED'}     

class SpherePreview(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_sphere"
    bl_label = ""    
    
    def execute(self, context):
        try: ActivePreview('Sphere')
        except: pass
        return {'FINISHED'}     

class CubePreview(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_cube"
    bl_label = ""    
    
    def execute(self, context):
        try: ActivePreview('Cube')
        except: pass
        return {'FINISHED'}
          
class PlanePreview(eval(api_functions['types_operator'])):
    bl_idname = "object.shadertoolsng_plane"
    bl_label = ""    
    
    def execute(self, context):
        try: ActivePreview('Plane')
        except: pass
        return {'FINISHED'}     

class ShadersToolsNGPanel(eval(api_functions['types_panel'])):
    bl_label = active_languages['panel_name']
    bl_idname = "OBJECT_PT_shaderstoolsng"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    ctx_props = eval(api_functions['props'])
    types_scene = eval(api_functions['types_scene'])
   
    #Open and save buttons in panel
    OpenSaveItems = SwitchButtonsList(("buttons_open", "buttons_save"))
    OpenSave = ctx_props.EnumProperty( name = "OpenSave", items = OpenSaveItems, update=OpenSaveSwitch)
    types_scene.shadertoolsng_open_save = OpenSave
    #Export and import buttons in panel
    ExportImportItems = SwitchButtonsList(("buttons_export", "buttons_import"))
    ExportImport = ctx_props.EnumProperty( name = "ExportImport", items = ExportImportItems, update=ExportImportSwitch)
    types_scene.shadertoolsng_export_import = ExportImport
    #Utils button in panel
    UtilsItems = SwitchButtonsList(("buttons_config", "buttons_create", "buttons_log", "buttons_help", "buttons_credits", "menu_utils_migrate", 
                                                        "buttons_tools_cleanup",  "buttons_addon_folder_access",  "buttons_export_import"))
    UtilsEnum = ctx_props.EnumProperty( name = "", items = UtilsItems, update=UtilsSwitch)
    UtilsProgressBar = ctx_props.IntProperty( name = "",  subtype='PERCENTAGE',  options={'ANIMATABLE'},  min=0,  max=100,  default=0,  update=UpdateProgressBar)
    types_scene.shadertoolsng_utils_bar = UtilsProgressBar
    types_scene.shadertoolsng_utils_enum = UtilsEnum

    def draw(self, context):
        ctx_scene = eval(api_functions['context_scene'])
        layout = self.layout
        row = layout.row()
    
        try:
            workbase_path = os.path.join(default_paths['temp'],  'workbase.blend')
            workbase_path_exists =  os.path.exists(workbase_path)
            if workbase_path_exists and  bpy.data.filepath == workbase_path:
                row.operator("object.shadertoolsng_suzanne", text="", icon="MONKEY" )
                row.operator("object.shadertoolsng_sphere", text="", icon="MESH_UVSPHERE" )
                row.operator("object.shadertoolsng_cube", text="", icon="MESH_CUBE" )
                row.operator("object.shadertoolsng_plane", text="", icon="MESH_PLANE" )
                row.operator("render.render", text=active_languages['menu_new_render'], icon="RENDER_STILL" )
                row = layout.row()
        except:pass
        if update: row.operator("object.shadertoolsng_warning", text=active_languages['menu_error_error001'], icon="RADIO")
        else:
            row.label("%s : " % active_languages['panel_database_label'], icon="SCENE_DATA")
            row.prop(ctx_scene, "shadertoolsng_open_save", expand=True)
            row = layout.row()
            row.label("%s : " % active_languages['panel_archive_label'], icon="NEW")
            row.prop(ctx_scene, "shadertoolsng_export_import", expand=True)
            row = layout.row()
            row.label("%s : " % active_languages['panel_utils_label'], icon="PREFERENCES")
            row.prop(ctx_scene, "shadertoolsng_utils_enum")
            if progress_bar:
                row = layout.row()
                row.prop(ctx_scene, "shadertoolsng_utils_bar")
            
MyReg = \
    (
     ShadersToolsNGPanel, Open, Save, Export, Import,New, Configuration, Help, Credits, UpdateWarning,
     ConfigurationSearch, Errors, UtilsMigrate, BeforeOpen, RestoreFilters, Informations, BeforeInformations,
     InformationsWeblink, OpenAddOnFolder, Cleanup, ExportImportDatabase, BeforeRemoveMaterial, RemoveMaterial,
     SuzannePreview, CubePreview,  SpherePreview,  PlanePreview,
    )

def register():
    try:
        for c in MyReg :
            bpy.utils.register_class(c)
        #end 
        print(misc.ConsoleError("Panel ", 0, True))
        print("*"*78)
        misc.LogError("*"*78, False)
    except:
        print(misc.ConsoleError("Panel ", 0, False))
#end register
def unregister():
    for c in MyReg :
        bpy.utils.unregister_class(c)
    #end for
#end unregister
if __name__ == "__main__":
    register()
    
    
