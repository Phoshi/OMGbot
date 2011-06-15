# -*- coding: utf-8 -*-
class plugin(object):
    def __init__(self):
        pass
    def __level__(self):
        return 0
    def disallowed(self,complete):
        return ["PRIVMSG $C$ :You do not have the access rights for that!"]
    def __init_db_tables__(self,name):
        pass
    def __append_seperator__(self):
        return False

