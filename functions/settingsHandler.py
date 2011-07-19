# -*- coding: utf-8 -*-
#!/usr/bin/python
import sqlite3
import os
import globalv
db=sqlite3.connect(os.path.join("config",globalv.database))
c=db.cursor()
def executeQuery(query):
    c.execute(query)
    return c.fetchall()
def readSetting(table,setting, where="1==1"):
    args=(setting,table,where)
    c.execute("SELECT %s FROM %s WHERE %s" % args)
    results=[]
    for row in c:
        results.append(row)
    if len(results)==1:
        results=results[0]
    if len(results)==1:
        results=results[0]
    return results
def readSettingRaw(table,setting, where="1==1"):
    args=(setting,table,where)
    c.execute("SELECT %s FROM %s WHERE %s" % args)
    results=[]
    for row in c:
        results.append(row)
    return results
def deleteSetting(table, setting, where):
    args=(table, setting)
    c.execute("DELETE FROM %s WHERE %s = ?"%args,(where,))
    db.commit()
def updateSetting(table, setting, value, where="1==1"):
    args=(table,setting, where)
    c.execute("UPDATE %s SET %s=? WHERE %s"%args,(value,))
    db.commit()
def readColumns(table):
    c.execute("pragma table_info(%s)"%(table))
    return [columnInfo[1] for columnInfo in c.fetchall()]
def writeSetting(table, settings, values):
    columns=[]
    if type(settings) is list:
        for setting in settings:
            columns.append('"'+setting+'"')
        settings=', '.join(columns)
    else:
        settings='"'+settings+'"'
    rows=[]
    if type(values) is list:
        for value in values:
            rows.append('"'+value.replace('"','""')+'"')
        values=', '.join(rows)
    else:
        values='"'+values+'"'
    args=(table,settings, values)
    c.execute("INSERT INTO %s (%s) VALUES (%s)" % args)
    db.commit()
def tableExists(table):
    try:
        c.execute("SELECT 1 FROM %s WHERE 1=0"%table)
        return 1
    except:
        return 0
def newTable(table,*args):
    arguments=[]
    values=[]
    for arg in args:
        arguments.append(arg)
    arguments=', '.join(arguments)
    args={"table":table,"arguments":arguments}
    c.execute('''CREATE TABLE %(table)s 
    (%(arguments)s)'''%args)
    db.commit()
def dropTable(table):
    c.execute("DROP TABLE %s" % table)
    db.commit()
def closeConnection():
    c.close()
def openConnection():
    db=sqlite3.connect("config\\config.db")
    c=db.cursor()
if __name__=="__main__":
    newTable("coreAutoJoin","channel")
    writeSetting("coreAutoJoin","channel","#metconst")
    writeSetting("coreAutoJoin","channel","#sr388")
