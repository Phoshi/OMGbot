import re

from plugins import plugin
import globalv

__version__ = '0.2.1'

cs_re = re.compile(r',\s+')
bks_re = re.compile(r'\[[0-9a-z]{2}\]')
prs_re = re.compile(r'\([0-9a-z]{2}(?:,[xy]\)|,s\),y|\))?')
jmp6_re = re.compile(r'\[[0-9a-z]{6}\]')
jmp4_re = re.compile(r'\([0-9a-z]{4}(?:,x)?\)')
label_re = re.compile(r'([\w\d]+):')
splitup_re = re.compile(r'..')

class pluginClass(plugin):

    def asm(self, token, tokens, labels):
        m = label_re.match(token)
        if m is not None:
            labels[m.group(1)] = len(tokens)
            token = token.split(None, 1)[1:]
        del m
        L = cs_re.sub(',', token).split()
        insn = L[0]
        if insn == 'db' or insn == 'data':
            return reduce(lambda x, y: x + y, [self.splitup(i) for i in L[1:]])
        if len(L) == 1:
            if insn == 'inx':
                return ['E8']
            if insn == 'iny':
                return ['C8']
            if insn == 'dex':
                return ['CA']
            if insn == 'dey':
                return ['88']
            if insn == 'pla':
                return ['68']
            if insn == 'plx':
                return ['FA']
            if insn == 'ply':
                return ['7A']
            if insn == 'pld':
                return ['2B']
            if insn == 'plb':
                return ['AB']
            if insn == 'plp':
                return ['28']
            if insn == 'tax':
                return ['AA']
            if insn == 'tay':
                return ['A8']
            if insn == 'tcs':
                return ['1B']
            if insn == 'tcd':
                return ['5B']
            if insn == 'txa':
                return ['8A']
            if insn == 'txy':
                return ['9B']
            if insn == 'txs':
                return ['9A']
            if insn == 'tya':
                return ['98']
            if insn == 'tyx':
                return ['BB']
            if insn == 'tsc':
                return ['3B']
            if insn == 'tsx':
                return ['BA']
            if insn == 'tdc':
                return ['7B']
            if insn == 'xba':
                return ['EB']
            if insn == 'clc':
                return ['18']
            if insn == 'cld':
                return ['D8']
            if insn == 'cli':
                return ['58']
            if insn == 'clv':
                return ['B8']
            if insn == 'sec':
                return ['38']
            if insn == 'sed':
                return ['F8']
            if insn == 'sei':
                return ['78']
            if insn == 'xce':
                return ['FB']
            if insn == 'nop':
                return ['EA']
            if insn == 'wdm':
                return ['42']
            if insn == 'rti':
                return ['40']
            if insn == 'rts':
                return ['60']
            if insn == 'rtl':
                return ['6B']
            if insn == 'wai':
                return ['CB']
            if insn == 'stp':
                return ['DB']
            if insn == 'pha':
                return ['48']
            if insn == 'php':
                return ['08']
            if insn == 'phx':
                return ['DA']
            if insn == 'phy':
                return ['5A']
            if insn == 'phb':
                return ['8B']
            if insn == 'phd':
                return ['0B']
            if insn == 'phk':
                return ['4B']
        if len(L) == 2:
            op = L[1]
            if insn == 'adc':
                if op[0] == '#':
                    return ['69'] + self.splitup(op[1:])
                if bks_re.match(op):
                    if op.endswith(',y'):
                        return ['77', op[1:3]]
                    return ['67', op[1:3]]
                if prs_re.match(op):
                    if op.endswith(',y'):
                        return ['73', op[1:3]]
                    if op.endswith(',x)'):
                        return ['61', op[1:3]]
                    if op.endswith(',y)'):
                        return ['71', op[1:3]]
                    return ['72', op[1:3]]
                if op.endswith(',x'):
                    op = op.rsplit(',', 1)[0]
                    b = self.splitup(op)
                    if len(b) == 1:
                        return ['75', b[0]]
                    if len(b) == 2:
                        return ['7D'] + b
                    if len(b) == 3:
                        return ['7F'] + b
                    return [None]
                if op.endswith(',y'):
                    return ['79'] + self.splitup(op[:-2])
                if op.endswith(',s'):
                    return ['63'] + self.splitup(op[:-2])
                b = self.splitup(op)
                if len(op) == 1:
                    return ['65', b[0]]
                if len(op) == 2:
                    return ['6D'] + b
                if len(op) == 3:
                    return ['6F'] + b
                return [None]
            if insn == 'inc':
                if op == 'a':
                    return ['1A']
                if op.endswith(',x'):
                    if len(op) == 4:
                        return ['F6', op[:2]]
                    if len(op) == 6:
                        return ['FE'] + self.splitup(op[:4])
                    return [None]
                if len(op) == 2:
                    return ['E6', op]
                if len(op) == 4:
                    return ['EE'] + self.splitup(op)
                return [None]
            if insn == 'sbc':
                if op[0] == '#':
                    return ['E9'] + self.splitup(op[1:])
                if bks_re.match(op):
                    if op.endswith(',y'):
                        return ['F7', op[1:3]]
                    return ['E7', op[1:3]]
                if prs_re.match(op):
                    if op.endswith(',y'):
                        return ['F3', op[1:3]]
                    if op.endswith(',x)'):
                        return ['E1', op[1:3]]
                    if op.endswith(',y)'):
                        return ['F1', op[1:3]]
                    return ['F2', op[1:3]]
                if op.endswith(',x'):
                    op = op.rsplit(',', 1)[0]
                    b = self.splitup(op)
                    if len(b) == 1:
                        return ['F5', b[0]]
                    if len(b) == 2:
                        return ['FD'] + b
                    if len(b) == 3:
                        return ['FF'] + b
                    return [None]
                if op.endswith(',y'):
                    return ['F9'] + self.splitup(op[:-2])
                if op.endswith(',s'):
                    return ['E3'] + self.splitup(op[:-2])
                b = self.splitup(op)
                if len(op) == 1:
                    return ['E5', b[0]]
                if len(op) == 2:
                    return ['ED'] + b
                if len(op) == 3:
                    return ['EF'] + b
                return [None]
            if insn == 'cmp':
                if op[0] == '#':
                    return ['C9'] + self.splitup(op[1:])
                if bks_re.match(op):
                    if op.endswith(',y'):
                        return ['D7', op[1:3]]
                    return ['C7', op[1:3]]
                if prs_re.match(op):
                    if op.endswith(',y'):
                        return ['D3', op[1:3]]
                    if op.endswith(',x)'):
                        return ['C1', op[1:3]]
                    if op.endswith(',y)'):
                        return ['D1', op[1:3]]
                    return ['D2', op[1:3]]
                if op.endswith(',x'):
                    op = op.rsplit(',', 1)[0]
                    b = self.splitup(op)
                    if len(b) == 1:
                        return ['D5', b[0]]
                    if len(b) == 2:
                        return ['DD'] + b
                    if len(b) == 3:
                        return ['DF'] + b
                    return [None]
                if op.endswith(',y'):
                    return ['D9'] + self.splitup(op[:-2])
                if op.endswith(',s'):
                    return ['C3'] + self.splitup(op[:-2])
                b = self.splitup(op)
                if len(op) == 1:
                    return ['C5', b[0]]
                if len(op) == 2:
                    return ['CD'] + b
                if len(op) == 3:
                    return ['CF'] + b
                return [None]
            if insn == 'cpx':
                if op[0] == '#':
                    return ['E0'] + self.splitup(op[1:])
                if len(op) == 2:
                    return ['E4', op]
                if len(op) == 4:
                    return ['EC'] + self.splitup(op)
                return [None]
            if insn == 'cpy':
                if op[0] == '#':
                    return ['C0'] + self.splitup(op[1:])
                if len(op) == 2:
                    return ['C4', op]
                if len(op) == 4:
                    return ['CC'] + self.splitup(op)
                return [None]
            if insn == 'dec':
                if op == 'a':
                    return ['3A']
                if op.endswith(',x'):
                    if len(op) == 4:
                        return ['D6', op[:2]]
                    if len(op) == 6:
                        return ['DE'] + self.splitup(op[:4])
                    return [None]
                if len(op) == 2:
                    return ['C6', op]
                if len(op) == 4:
                    return ['CE'] + self.splitup(op)
                return [None]
            if insn == 'lda':
                if op[0] == '#':
                    return ['A9'] + self.splitup(op[1:])
                if bks_re.match(op):
                    if op.endswith(',y'):
                        return ['B7', op[1:3]]
                    return ['A7', op[1:3]]
                if prs_re.match(op):
                    if op.endswith(',y'):
                        return ['B3', op[1:3]]
                    if op.endswith(',x)'):
                        return ['A1', op[1:3]]
                    if op.endswith(',y)'):
                        return ['B1', op[1:3]]
                    return ['B2', op[1:3]]
                if op.endswith(',x'):
                    op = op.rsplit(',', 1)[0]
                    b = self.splitup(op)
                    if len(b) == 1:
                        return ['B5', b[0]]
                    if len(b) == 2:
                        return ['BD'] + b
                    if len(b) == 3:
                        return ['BF'] + b
                    return [None]
                if op.endswith(',y'):
                    return ['B9'] + self.splitup(op[:-2])
                if op.endswith(',s'):
                    return ['A3'] + self.splitup(op[:-2])
                b = self.splitup(op)
                if len(op) == 1:
                    return ['A5', b[0]]
                if len(op) == 2:
                    return ['AD'] + b
                if len(op) == 3:
                    return ['AF'] + b
                return [None]
            if insn == 'ldx':
                if op[0] == '#':
                    return ['A2'] + self.splitup(op[1:])
                if len(op) == 2:
                    return ['A6', op]
                if len(op) == 4:
                    return ['AE'] + self.splitup(op)
                return [None]
            if insn == 'ldy':
                if op[0] == '#':
                    return ['A0'] + self.splitup(op[1:])
                if len(op) == 2:
                    return ['A4', op]
                if len(op) == 4:
                    return ['AC'] + self.splitup(op)
                return [None]
            if insn == 'ora':
                if op[0] == '#':
                    return ['09'] + self.splitup(op[1:])
                if bks_re.match(op):
                    if op.endswith(',y'):
                        return ['17', op[1:3]]
                    return ['07', op[1:3]]
                if prs_re.match(op):
                    if op.endswith(',y'):
                        return ['13', op[1:3]]
                    if op.endswith(',x)'):
                        return ['01', op[1:3]]
                    if op.endswith(',y)'):
                        return ['11', op[1:3]]
                    return ['12', op[1:3]]
                if op.endswith(',x'):
                    op = op.rsplit(',', 1)[0]
                    b = self.splitup(op)
                    if len(b) == 1:
                        return ['15', b[0]]
                    if len(b) == 2:
                        return ['1D'] + b
                    if len(b) == 3:
                        return ['1F'] + b
                    return [None]
                if op.endswith(',y'):
                    return ['19'] + self.splitup(op[:-2])
                if op.endswith(',s'):
                    return ['03'] + self.splitup(op[:-2])
                b = self.splitup(op)
                if len(op) == 1:
                    return ['05', b[0]]
                if len(op) == 2:
                    return ['0D'] + b
                if len(op) == 3:
                    return ['0F'] + b
                return [None]
            if insn == 'and':
                if op[0] == '#':
                    return ['29'] + self.splitup(op[1:])
                if bks_re.match(op):
                    if op.endswith(',y'):
                        return ['37', op[1:3]]
                    return ['27', op[1:3]]
                if prs_re.match(op):
                    if op.endswith(',y'):
                        return ['33', op[1:3]]
                    if op.endswith(',x)'):
                        return ['21', op[1:3]]
                    if op.endswith(',y)'):
                        return ['31', op[1:3]]
                    return ['32', op[1:3]]
                if op.endswith(',x'):
                    op = op.rsplit(',', 1)[0]
                    b = self.splitup(op)
                    if len(b) == 1:
                        return ['35', b[0]]
                    if len(b) == 2:
                        return ['3D'] + b
                    if len(b) == 3:
                        return ['3F'] + b
                    return [None]
                if op.endswith(',y'):
                    return ['39'] + self.splitup(op[:-2])
                if op.endswith(',s'):
                    return ['23'] + self.splitup(op[:-2])
                b = self.splitup(op)
                if len(op) == 1:
                    return ['25', b[0]]
                if len(op) == 2:
                    return ['2D'] + b
                if len(op) == 3:
                    return ['2F'] + b
                return [None]
            if insn == 'bit':
                if op[0] == '#':
                    return ['89'] + self.splitup(op[1:])
                if op.endswith(',x'):
                    if len(op) == 4:
                        return ['34', op[:2]]
                    if len(op) == 6:
                        return ['3C'] + self.splitup(op[:4])
                    return [None]
                if len(op) == 2:
                    return ['24', op]
                if len(op) == 4:
                    return ['2C'] + self.splitup(op)
                return [None]
            if insn == 'eor':
                if op[0] == '#':
                    return ['49'] + self.splitup(op[1:])
                if bks_re.match(op):
                    if op.endswith(',y'):
                        return ['57', op[1:3]]
                    return ['47', op[1:3]]
                if prs_re.match(op):
                    if op.endswith(',y'):
                        return ['53', op[1:3]]
                    if op.endswith(',x)'):
                        return ['41', op[1:3]]
                    if op.endswith(',y)'):
                        return ['51', op[1:3]]
                    return ['52', op[1:3]]
                if op.endswith(',x'):
                    op = op.rsplit(',', 1)[0]
                    b = self.splitup(op)
                    if len(b) == 1:
                        return ['55', b[0]]
                    if len(b) == 2:
                        return ['5D'] + b
                    if len(b) == 3:
                        return ['5F'] + b
                    return [None]
                if op.endswith(',y'):
                    return ['59'] + self.splitup(op[:-2])
                if op.endswith(',s'):
                    return ['43'] + self.splitup(op[:-2])
                b = self.splitup(op)
                if len(op) == 1:
                    return ['45', b[0]]
                if len(op) == 2:
                    return ['4D'] + b
                if len(op) == 3:
                    return ['4F'] + b
                return [None]
            if insn == 'asl':
                if op == 'a':
                    return ['0A']
                if op.endswith(',x'):
                    if len(op) == 4:
                        return ['16', op[:2]]
                    if len(op) == 6:
                        return ['1E'] + self.splitup(op[:4])
                    return [None]
                if len(op) == 2:
                    return ['06', op]
                if len(op) == 4:
                    return ['0E'] + self.splitup(op)
                return [None]
            if insn == 'rol':
                if op == 'a':
                    return ['2A']
                if op.endswith(',x'):
                    if len(op) == 4:
                        return ['36', op[:2]]
                    if len(op) == 6:
                        return ['3E'] + self.splitup(op[:4])
                    return [None]
                if len(op) == 2:
                    return ['26', op]
                if len(op) == 4:
                    return ['2E'] + self.splitup(op)
                return [None]
            if insn == 'lsr':
                if op == 'a':
                    return ['4A']
                if op.endswith(',x'):
                    if len(op) == 4:
                        return ['56', op[:2]]
                    if len(op) == 6:
                        return ['5E'] + self.splitup(op[:4])
                    return [None]
                if len(op) == 2:
                    return ['46', op]
                if len(op) == 4:
                    return ['4E'] + self.splitup(op)
                return [None]
            if insn == 'ror':
                if op == 'a':
                    return ['6A']
                if op.endswith(',x'):
                    if len(op) == 4:
                        return ['76', op[:2]]
                    if len(op) == 6:
                        return ['7E'] + self.splitup(op[:4])
                    return [None]
                if len(op) == 2:
                    return ['66', op]
                if len(op) == 4:
                    return ['6E'] + self.splitup(op)
                return [None]
            if insn == 'sep':
                if op[0] == '#':
                    return ['E2', op[1:3]]
                return [None]
            if insn == 'rep':
                if op[0] == '#':
                    return ['C2', op[1:3]]
                return [None]
            if insn == 'jmp':
                if jmp6_re.match(op):
                    return ['DC'] + self.splitup(op[1:-1])
                if jpm4_re.match(op):
                    if op.endswith(',x)'):
                        return ['7C'] + self.splitup(op[1:5])
                    return ['6C'] + self.splitup(op[1:5])
                if len(op) == 4:
                    return ['4C'] + self.splitup(op)
                if len(op) == 6:
                    return ['5C'] + self.splitup(op)
                return [None]
            if insn == 'jml':
                return ['5C'] + self.splitup(op)
            if insn == 'jsr':
                if insn.startswith('(') and insn.endswith(',x)'):
                    return ['FC'] + self.splitup(op[1:5])
                if len(insn) == 4:
                    return ['20'] + self.splitup(op)
                if len(insn) == 6:
                    return ['22'] + self.splitup(op)
                return [None]
            if insn == 'jsl':
                return ['22'] + self.splitup(op)
            if insn == 'bra':
                if op in labels:
                    return ['label ' + token, '']
                if len(op) == 2:
                    return ['80', op]
                return [None]
            if insn == 'brl':
                if op in labels:
                    return ['label ' + token, '', '']
                return ['82'] + self.splitup(op)
            if insn == 'bcc':
                if op in labels:
                    return ['label ' + token, '']
                return ['90', op]
            if insn == 'bcs':
                if op in labels:
                    return ['label ' + token, '']
                return ['B0', op]
            if insn == 'beq':
                if op in labels:
                    return ['label ' + token, '']
                return ['F0', op]
            if insn == 'bne':
                if op in labels:
                    return ['label ' + token, '']
                return ['D0', op]
            if insn == 'bmi':
                if op in labels:
                    return ['label ' + token, '']
                return ['30', op]
            if insn == 'bpl':
                if op in labels:
                    return ['label ' + token, '']
                return ['10', op]
            if insn == 'bvc':
                if op in labels:
                    return ['label ' + token, '']
                return ['50', op]
            if insn == 'bvs':
                if op in labels:
                    return ['label ' + token, '']
                return ['70', op]
            if insn == 'cop':
                return ['02', op]
            if insn == 'brk':
                return ['00', op]
            if insn == 'sta':
                if bks_re.match(op):
                    if op.endswith(',y'):
                        return ['97', op[1:3]]
                    return ['87', op[1:3]]
                if prs_re.match(op):
                    if op.endswith(',y'):
                        return ['93', op[1:3]]
                    if op.endswith(',x)'):
                        return ['81', op[1:3]]
                    if op.endswith(',y)'):
                        return ['91', op[1:3]]
                    return ['92', op[1:3]]
                if op.endswith(',x'):
                    op = op.rsplit(',', 1)[0]
                    b = self.splitup(op)
                    if len(b) == 1:
                        return ['95', b[0]]
                    if len(b) == 2:
                        return ['9D'] + b
                    if len(b) == 3:
                        return ['9F'] + b
                    return [None]
                if op.endswith(',y'):
                    return ['99'] + self.splitup(op[:-2])
                if op.endswith(',s'):
                    return ['83'] + self.splitup(op[:-2])
                b = self.splitup(op)
                if len(op) == 1:
                    return ['85', b[0]]
                if len(op) == 2:
                    return ['8D'] + b
                if len(op) == 3:
                    return ['8F'] + b
                return [None]
            if insn == 'stx':
                if op.endswith(',y'):
                    return ['96', op[:2]]
                if len(op) == 2:
                    return ['86', op]
                if len(op) == 4:
                    return ['8E'] + self.splitup(op)
                return [None]
            if insn == 'sty':
                if op.endswith(',x'):
                    return ['94', op[:2]]
                if len(op) == 2:
                    return ['84', op]
                if len(op) == 4:
                    return ['8C'] + self.splitup(op)
                return [None]
            if insn == 'stz':
                if op.endswith(',x'):
                    if len(op) == 4:
                        return ['74', op[:2]]
                    if len(op) == 6:
                        return ['9E'] + self.splitup(op[:4])
                    return [None]
                if len(op) == 2:
                    return ['64', op]
                if len(op) == 4:
                    return ['9C'] + self.splitup(op)
                return [None]
            if insn == 'tsb':
                if len(op) == 2:
                    return ['04', op]
                if len(op) == 4:
                    return ['0C'] + self.splitup(op)
                return [None]
            if insn == 'trb':
                if len(op) == 2:
                    return ['14', op]
                if len(op) == 4:
                    return ['1C'] + self.splitup(op)
                return [None]
            if insn == 'pea':
                return ['F4'] + self.splitup(op)
            if insn == 'pei':
                return ['D4'] + self.splitup(op)
            if insn == 'per':
                return ['62'] + self.splitup(op)
            return [None]
        if len(L) == 3:
            if insn == 'mvn':
                return ['54', L[2], L[1]]
            if insn == 'mvp':
                return ['44', L[2], L[1]]
            return [None]
        return [None]

    def splitup(self, op):
        return splitup_re.findall('0' + op if len(op) & 1 else op)
    
    def gettype(self):
        return 'command'
    
    def action(self, complete):
        msg = []
        tokens = complete.message().lower().replace('$', '').split(';')
        labels = {}
        for i in xrange(len(tokens)):
            token = tokens[i].strip()
            m = label_re.match(token)
            if m is not None:
                labels[m.group(1)] = None
        for token in tokens:
            token = token.strip()
            asm = self.asm(token, msg, labels)
            if None in asm:
                return ['PRIVMSG $C$ :Error: failed token: ' + token]
            msg.extend(asm)
        for i in xrange(len(msg)):
            token = msg[i]
            if token.startswith('label '):
                subs = tuple(token[6:].split())
                label = labels[subs[1]]
                print 'subs: %r   label: %r   i: %r' % (subs, label, i)
                if subs[0] == 'brl':
                    delta = label - (i + 3)
                    if not (delta &~ 65535):
                        b = self.splitup(hex(delta & 65535)[2:].zfill(4))
                        msg[i] = '82'
                        msg[i + 1] = b[0]
                        msg[i + 2] = b[1]
                        continue
                    else:
                        return ['PRIVMSG $C$ :Error: label too far: brl ' +
                                subs[1]]
                delta = label - (i + 2)
                if not (delta &~ 255):
                    b = subs[0] + ' ' + hex(delta & 255)[2:].zfill(2)
                    print repr(b)
                    msg[i:i + 2] = self.asm(b, msg, labels)
                    continue
                else:
                    return ['PRIVMSG $C$ :Error: label too far: %s %s' % subs]
        print 'msg: %r' % msg
        return ['PRIVMSG $C$ :' + ' '.join(msg).upper()]
    
    def describe(self, complete):
        return [
            'PRIVMSG $C$ :65816 Assembler Module version %s' % __version__,
            'PRIVMSG $C$ :Copyright 2011 Branden Brown (a.k.a. zephyrtronium, '
            'uNsane, smlaxy, etc.)',
            "PRIVMSG $C$ :PJBoy's 65816 opcode list was referenced in order "
            'to write this: http://interdpth.arc-nova.org/PJs%20stuff/Lists'
            '/65816%20opcodes.txt',
            ]
