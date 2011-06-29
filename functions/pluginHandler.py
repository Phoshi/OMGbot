# -*- coding: utf-8 -*-
import globalv
import shlex
import settingsHandler
def load_plugin(input, loadAs=""): #Loads a plugin, placing it in it's correct category.
    state=0
    #arguments=shlex.split(' '.join(input.split()[1:]))
    name=input.split()[0]
    x=__import__(name)
    if loadAs!="":
        name=loadAs
    else:
        loadAs = name
    if name in globalv.loadedPlugins:
        state=1
    if name in globalv.loadedRealtime:
        state=1
    if name in globalv.loadedSpecial:
        state=1
    reload(x)
    y=x.pluginClass()
    if y.gettype()=="command":
        globalv.loadedPlugins.update({name:y})
    if y.gettype()=="realtime":
        globalv.loadedRealtime.update({name:y})
    if y.gettype()=="special":
        globalv.loadedSpecial.update({name:y})
    if y.gettype()=="preprocess":
        globalv.loadedPreprocess.update({name:y})
    if y.gettype()=="postprocess":
        globalv.loadedPostprocess.update({name:y})
    globalv.aliasExtensions.update({name:''})
    if settingsHandler.tableExists(name)==0:
        y.__init_db_tables__(name)
    if name not in [x[0] for x in settingsHandler.readSetting("'core-userlevels'", "plugin")]:
        settingsHandler.writeSetting("'core-userlevels'", ["plugin", "level"],[name, str(y.__level__())])
    globalv.basePlugin[loadAs]=input.split()[0]
    return state
def rename_plugin(name, newName):
    if (newName not in globalv.loadedPlugins.keys()):
        return False
    if (name not in globalv.basePlugin.keys()):
        return False
    unload_plugin(name)
    load_plugin(globalv.basePlugin[name], newName)
    return True
def unload_plugin(name): #Unloads a plugin (A bit dirty, but it works)
    success=1
    if name in globalv.loadedPlugins.keys():
        del globalv.loadedPlugins[name]
    elif name in globalv.loadedRealtime.keys():
        del globalv.loadedRealtime[name]
    elif name in globalv.loadedSpecial.keys():
        del globalv.loadedSpecial[name]
    elif name in globalv.loadedPreprocess.keys():
        del globalv.loadedPreprocess[name]
    elif name in globalv.loadedPostprocess.keys():
        del globalv.loadedPostprocess[name]
    else:
        success=0
    return success
