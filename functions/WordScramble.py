#WordScramble.py
################
#Scramble the middle bits of words
def scramble(words):
    import random
    import re
    words=words.split()
    for index, word in enumerate(words):
        punctuation=re.findall("^([^a-zA-Z0-9]*)([a-zA-Z0-9']+)([^a-zA-Z0-9]*)", word)
        if len(punctuation)==0:
            continue
        else:
            punctuation=punctuation[0]
        word=list(punctuation[1])
        if len(word)<=1:
            continue
        firstLetter=word[0]
        lastLetter=word[-1]
        middle=word[1:-1]
        random.shuffle(middle)
        word=punctuation[0]+firstLetter+''.join(middle)+lastLetter+punctuation[-1]
        words[index]=word
    return ' '.join(words)
