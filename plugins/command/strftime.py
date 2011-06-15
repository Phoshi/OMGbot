# -*- coding: utf-8 -*-
from plugins import plugin
import time
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        timezones={'FNT': -2, 'AKDT': -8, 'GST': 4, 'CCT': 6, 'LINT': 14, 'BOT': -4, 'EGT': -1, 'CKT': -10, 'DAVT': 7, 'WDT': 9, 'WITA': 8, 'X': -11, 'TMT': 5, 'KUYT': 4, 'Z': 0, 'PETT': 12, 'PDT': -7, 'IOT': 6, 'NZDT': 13, 'MYT': 8, 'HKT': 8, 'PET': -5, 'PMDT': -2, 'NOVST': 7, 'AMST': -3, 'PMST': -3, 'MAWT': 5, 'FJST': 13, 'D': 4, 'HAA': -3, 'HAC': -5, 'HAE': -4, 'BNT': 8, 'HAY': -8, 'T': -7, 'WET': 0, 'HAP': -7,'NZST': 12, 'HAR': -6, 'OMSST': 7, 'HAT': -2, 'BRST': -2, 'PT': -8, 'ANAT': 12,'CXT': 7, 'UYT': -3, 'VLAST': 11, 'HOVT': 7, 'PYT': -4, 'ALMT': 6, 'WT': 0, 'IRKST': 9, 'NPT': 5, 'HNT': -3, 'KST': 9, 'Y': -12, 'EET': 2, 'LHDT': 11, 'VLAT': 10, 'LHST': 10, 'AZST': 5, 'WFT': 12, 'MART': -9, 'PHOT': 13, 'PKT': 5, 'GET': 4, 'YEKT': 5, 'EGST': 0, 'TKT': -10, 'CET': 1, 'EEST': 3, 'SCT': 4, 'AMT': -4, 'ChST': 10, 'C': 3, 'G': 7, 'K': 10, 'O': -2, 'MAGT': 11, 'WGT': -3, 'S': -6, 'NFT': 11, 'W': -10, 'AFT': 4, 'ET': -5, 'MHT': 12, 'BTT': 6, 'HLV': -4, 'YAKST': 10, 'TJT': 5, 'TVT': 12, 'PHT': 8, 'HADT': -9, 'PST': -8, 'HNA': -4, 'MUT': 4, 'HNC': -6, 'GAMT': -9, 'HNE': -5, 'COT': -5, 'IRST': 3, 'UYST': -2, 'IDT': 3, 'AZOST': 0, 'IRDT': 4, 'RET': 4, 'IST': 1, 'HNP': -8, 'VUT': 11, 'HNR': -7, 'CHAST': 12, 'CST': -6, 'HNY': -9, 'FJT': 12, 'IRKT': 8, 'SAST': 2, 'AST': -4, 'BST': 1, 'AZOT': -1, 'NUT': -11, 'JST': 9, 'CAST': 8, 'ANAST': 12, 'ECT': -5, 'MAGST': 12, 'AQTT': 5, 'YAPT': 10, 'EAST': -6, 'TAHT': -10, 'MDT': -6, 'GALT': -6, 'ADT': -3, 'B': 2, 'CLST': -3, 'F': 6, 'OMST': 6, 'CLT': -4, 'N': -1, 'R': -5, 'SRT': -3, 'V': -9, 'GILT': 12, 'WAT': 1, 'NDT': -2, 'GMT': 0, 'WIB': 7, 'SBT': 11, 'PYST': -3, 'MMT': 6, 'BRT': -3, 'YAKT': 9, 'CDT': -5, 'WIT': 9, 'EDT': 11, 'SST': -11, 'WAST': 2, 'NOVT': 6, 'KRAST': 8, 'TFT': 5, 'ULAT': 8, 'KRAT': 7, 'PONT': 11, 'CVT': -1, 'MST': -7, 'VET': -4, 'CAT': 2, 'MSK': 3, 'WST': -11, 'MVT': 5, 'MSD': 4, 'AZT': 4, 'TLT': 9, 'SGT': 8, 'HAST': -10, 'AKST': -9, 'PGT': 10, 'GYT': -4, 'CEST': 2, 'H': 8, 'UZT': 5, 'NST': -3, 'EAT': 3, 'A': 1, 'YEKST': 6, 'EST':-5, 'E': 5, 'PETST': 12, 'I': 9, 'M': 12, 'L': 11, 'Q': -4, 'U': -8, 'CHADT': 13, 'FKST': -3, 'FKT': -4, 'ICT': 7, 'PWT': 9, 'ART': -3, 'KGT': 6, 'P': -3, 'WEST': 1, 'NCT': 11, 'GFT': -3, 'WGST': -2, 'EASST': -5, 'SAMT': 4}
        def isNumber(number):
            try:
                float(number)
                return True
            except ValueError:
                return False
        msg=complete.message()
        timestring=msg
        offset=0
        if len(msg.split())>1:
            offsetString=msg.split()[0]
            if isNumber(offsetString) or offsetString.upper() in timezones:
                if offsetString.upper() in timezones:
                    offset=timezones[offsetString.upper()]
                else:
                    offset=float(offsetString)
                offset=offset*(60*60)
                timestring=' '.join(msg.split()[1:])

        print time.daylight
        return ["PRIVMSG $C$ :%s"%time.strftime(timestring, time.gmtime(time.time()+offset))]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
