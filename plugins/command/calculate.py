# -*- coding: utf-8 -*-
from __future__ import division
import globalv
from plugins import plugin
from math import *
import urllib
import multiprocessing
import time
import WordScramble
from random import random, randint, shuffle
import ast
import re
finished=False
safe_list = ['random','math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'de grees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh','int','bin','oct','hex'] #use the list to filter the local namespace 
safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ]) #add any needed builtins back in.
safe_dict['abs'] = abs 
reload(WordScramble)
safe_dict['scramble']=WordScramble.scramble
safe_dict['hex']=hex
safe_dict['int']=int
safe_dict['oct']=oct
safe_dict['bin']=bin
safe_dict['len']=len
safe_dict['chr']=chr
safe_dict['True']=True
safe_dict['False']=False
safe_dict['randint']=randint
safe_dict['reduce']=reduce
safe_dict['factorial']=factorial
safe_dict['set']=set
safe_dict['str']=str
safe_dict['sorted']=sorted
safe_dict['sum']=sum
safe_dict['range']=xrange
safe_dict['urlescape']=urllib.quote
def notInPlaceShuffle(list):
    shuffle(list)
    return list
def int2base(x,b,alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
    'convert an integer to its string representation in a given base'
    #Credit to Mark Borgerding
    if b<2 or b>len(alphabet):
        if b==64: # assume base64 rather than raise error
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        else:
            raise AssertionError("int2base base out of range")
    if type(x) == complex: # return a tuple
        return ( int2base(x.real,b,alphabet) , int2base(x.imag,b,alphabet) )
    if x<=0:
        if x==0:
            return alphabet[0]
        else:
            return  '-' + int2base(-x,b,alphabet)
    # else x is non-negative real
    rets=''
    while x>0:
        x,idx = divmod(x,b)
        rets = alphabet[idx] + rets
    return rets
primes = [ # list of primes 2 < P <= 1009
        3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
        83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
        167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251,
        257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
        353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
        449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557,
        563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647,
        653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757,
        761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
        877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
        991, 997, 1009
        ]
def factorize(x):
    '''Return a list of the prime factors of x (including -1 if x is negative).'''
    if not x:
        return [0]
    if x in primes:
        return [x]
    if x < 0:
        a = [-1]
    else:
        a = []
    while not (x & 1):
        a.append(2)
        x >>= 1
    n = 0
    while n < len(primes):
        q, r = divmod(x, primes[n])
        if not r:
            a.append(primes[n])
            x = q
        else:
            n += 1
        c = 1013
        while x > 1:
            q, r = divmod(x, c)
            if not r:
                a.append(c)
                x = q
            else:
                c += 1
                while not isprime(c):
                    c += 1
    return a
def bite(x):
    '''Return a list of the powers of two that sum to x.
    All elements will have the same sign as x.'''
    c = -x if x < 0 else x # Twice as fast as c = abs(x). x >= 0 is faster than x < 0.
    a = []
    n = 1
    while n <= c:
        if c & n: # naive
            a.append(-n if x < 0 else n)
        n <<= 1
    return a if a else [0]
def isprime(x):
    '''Return True if the only unique factors of x are 1 and x.'''
    if x < 2:
        return False
    if x < 4:
        return True
    if not x & 1:
        return False
    if x in primes:
        return True
    if x < 1009:
        return False
    n = 0
    while n < len(primes):
        if not x % primes[n]:
            return False
        n += 1
    m = int(x ** 0.5) + 1 # ceil(sqrt(x))
    c = 1013
    while c < m:
        if not x % c:
            return False
        c += 1
        while not isprime(c): # should help reduce execution time for large numbers
            c += 1
    return True
safe_dict['factorise']=factorize
safe_dict['isprime']=isprime
safe_dict['bite']=bite
safe_dict['factorize']=factorize
safe_dict['int2base']=int2base
safe_dict['shuffle']=notInPlaceShuffle
def convertBitsToFloat(msg):
    allNums=re.findall("[0-9.]*",msg)
    for num in allNums:
        if num!='':
            try:
                msg.replace(num,str(float(num)))
            except:
                pass
    return msg
import ast
def evaluate(msg, output):
    rawStr = "%r"%msg
    print rawStr
    newDict = safe_dict.copy()
    newDict.update(globalv.variables)
    output.put(("%r"%(str(eval(msg,{"__builtins__":None},newDict))))[1:-1])

class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        msg=convertBitsToFloat(msg)
        try:
            outputQueue=multiprocessing.Queue()
            calculationThread=multiprocessing.Process(target=evaluate, args=(msg,outputQueue))
            calculationThread.start()
            now=time.time()
            while (time.time()-now)<5:
                time.sleep(0.05)
                if calculationThread.is_alive()==False and outputQueue.empty():
                    raise Exception(msg)
                if outputQueue.empty()==False:
                    msg=outputQueue.get()
                    break
            else:
                calculationThread.terminate()
                raise Exception("Calculation took too long!")
        except Exception as detail:
            msg="Calculation Failure: %s"%detail
        if len(msg)>8000:
            msg="Result far too large!"
        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !calculate module! I do maths!","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!calculate [expression]"]
