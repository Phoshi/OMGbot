# -*- coding: utf-8 -*-
from plugins import plugin
from datetime import datetime
from securityHandler import isAllowed
import globalv
import pickle
import os
import difflib

def days_till(date):
    now = datetime.now()
    now = now.replace(hour = 10)
    date = date.replace(hour = 11)
    
    if date.year == 1900:
        if date.month > now.month:
            date = date.replace(year = now.year)
        elif date.month < now.month:
            date = date.replace(year = now.year+1)
        else:
            if date.day > now.day:
                date = date.replace(year = now.year)
            elif date.day < now.day:
                date = date.replace(year = now.year+1)
            else:
                return 0
    return (date - now).days

def parse_date(date):
    if date.year != 1900:
        parsed = date.strftime("%B %d{S} %Y")
    else:
        parsed = date.strftime("%B %d{S}")

    day = date.day
    suffix = 'th' if 11 <= day <= 13 else {1:'st',2:'nd',3:'rd'}.get(day % 10, 'th')

    return parsed.replace("{S}", suffix)

def interpret_date(eventdate, formats):
    eventdate = eventdate.replace("gust","____").replace("st","").replace("nd","").replace("rd","").replace("th","").replace("____","gust")

    for dformat in formats:
        try:
            newdate = datetime.strptime(eventdate, dformat)
            return newdate
        except:
            pass
    return None

def remove_keys_lower(d, key):
    to_remove = []
    for e in d:
        if e.lower() == key:
            to_remove.append(e)
    for e in to_remove:
        del d[e]

class pluginClass(plugin):
    def __init__(self):
        self.formats = [
            "%Y-%m-%d",    #2017-03-31
            "%B %d, %Y",   #March 31, 2017
            "%B %d %Y",    #March 31 2017
            "%d %B %Y",    #31 March 2017
            "%d %B",       #31 March
            "%B %d"       #March 31
            ]
    def gettype(self):
        return "command"
    
    def output_remaining_days(self, date, events, events_lower):
        eventname_lower = date.lower()
        eventname = date
        
        event_exists = False
        if eventname_lower in events_lower:
            delta_days = days_till(events_lower[eventname_lower])
            for event in events:
                if event.lower() == eventname_lower:
                    eventname = event
                    break
            event_exists = True
        else:
            newdate = interpret_date(eventname, self.formats)
            if newdate:
                event_exists = True
                delta_days = days_till(newdate)

        if not event_exists:
            response = ["PRIVMSG $C$ :%s has not been set as an event yet." % eventname]
            close_matches = difflib.get_close_matches(eventname, events)
            if len(close_matches) > 0:
                response.append("PRIVMSG $C$ :Did you mean: " + ', '.join(close_matches))
            return response
            
        if delta_days == 0:
            return ["PRIVMSG $C$ :Today it's %s!" % eventname]
        elif delta_days < 0:
            return ["PRIVMSG $C$ :%s happened %d days ago." % (eventname, -delta_days)]
        else:
            return ["PRIVMSG $C$ :%d days till %s" % (delta_days, eventname)]
        
    def action(self, complete):
        print complete
        file_name = "events-%s"%complete.cmd()[0]
        file_path = os.path.join("config",file_name)

        events = {}
        
        if os.path.exists(file_path):
            with open(file_path) as event_file:
                events = dict(pickle.load(event_file))

        events_lower = dict(map(lambda (key,val): (key.lower(),val), events.items()))
                
        s = complete.message().split()

        command = s[0]
        
        if len(s) < 1:
            return ["PRIVMSG $C$ :Invalid parameters"]
        
        if command == "upcoming":
            upcoming = sorted([(event, date) for event, date in events.items() if days_till(date)>0], key = lambda (event, date): days_till(date))

            aa = "Upcoming: "

            for event in upcoming[:5]:
                aa += event[0] + " on " + parse_date(event[1]) + "; "
                
            return ["PRIVMSG $C$ :"+aa]
        
        if command == "till":
            return self.output_remaining_days(' '.join(s[1:]), events, events_lower)
        
        if command == "set" or command == "override":
            if not "as" in s:
                return ["PRIVMSG $C$ :Invalid usage; use: !countdown %s [Event name] as [Date]" % command]
                            
            split_pos = s.index("as")
            eventname = ' '.join(s[1:split_pos])
            ddate = ' '.join(s[split_pos+1:])

            eventname_lower = eventname.lower()

            if interpret_date(eventname, self.formats):
                return ["PRIVMSG $C$ :You are not allowed to set dates as event names."]

            newdate = interpret_date(ddate, self.formats)

            if eventname_lower in events_lower:
                if command == "set":
                    current_date = parse_date(events_lower[eventname_lower])
                    
                    response = ["PRIVMSG $C$ :That event has already been set at %s." % current_date]
                    if interpret_date(current_date, self.formats) != newdate:
                        response += ["Use \"!countdown override %s as %s\" to override" % (eventname, ddate)]
                    return response
            elif command == "override":
                response = ["PRIVMSG $C$ :%s has not been set as an event yet." % eventname]
                close_matches = difflib.get_close_matches(eventname, events)
                if len(close_matches) > 0:
                    response.append("PRIVMSG $C$ :Did you mean: " + ', '.join(close_matches))
                return response
                    
            if not newdate:
                return ["PRIVMSG $C$ :Invalid date format. Valid date formats: YYYY-mm-dd, Month dd(th)(,) (YYYY), dd Month"]
            
            remove_keys_lower(events, eventname_lower)
            events[eventname] = newdate
                        
            with open(file_path,"w") as event_file:
                pickle.dump(events, event_file)

            return ["PRIVMSG $C$ :%s successfully %s!" % (eventname, "added" if command == "set" else "updated")]

        if command == "remove":
            if isAllowed(complete.userMask()) < 150:
                return ["PRIVMSG $C$ :You don't have the privileges to remove events."]
            
            eventname = ' '.join(s[1:])
            eventname_lower = eventname.lower()

            if eventname_lower not in events_lower:
                response = ["PRIVMSG $C$ :%s has not been set as an event." % eventname]
                close_matches = difflib.get_close_matches(eventname, events)
                if len(close_matches) > 0:
                    response.append("PRIVMSG $C$ :Did you mean: " + ', '.join(close_matches))
                return response

            remove_keys_lower(events, eventname_lower)

            with open(file_path,"w") as event_file:
                pickle.dump(events, event_file)
                
            return ["PRIVMSG $C$ :Event successfully removed!"]

        return self.output_remaining_days(' '.join(s[0:]), events, events_lower)

    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !countdown module",
                "PRIVMSG $C$ :Usage:",
                "PRIVMSG $C$ :!countdown set [Event name] as [Date]",
                "PRIVMSG $C$ :!countdown (till) [Event name]"]
