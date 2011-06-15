import globalv
import settingsHandler
def getArguments(string, depth=0, startIndex=0):
    def reset():
        argumentStart=-1
        lowerDepths=[]
        argumentEnd=-1
        argumentDepth=0
        hasArguments=False
        start=-1
        end=-1
    #print "Starting parse on string: %s"%string
    positions=[] #In format (depth, start, length)
    lowerDepths=[]
    beginCharacter='$'
    breakCharacters=[' ']
    argumentCharacter=['(',')']
    argumentStart=-1
    argumentEnd=-1
    argumentDepth=0
    hasArguments=False
    commandName=""
    start=-1
    end=-1
    for index,letter in enumerate(string):
        if letter==beginCharacter:
            if start==-1:
                start=index
            elif not hasArguments or (hasArguments and string[index-1]==argumentCharacter[-1] and argumentDepth==0):
                end=index
                capturedString=string[start+1:end]
                print capturedString
                if capturedString.isdigit() or capturedString=="*":
                    argumentStart=-1
                    lowerDepths=[]
                    argumentEnd=-1
                    argumentDepth=0
                    hasArguments=False
                    start=-1
                    end=-1
                    print "Reset, continuing"
                    continue
                if hasArguments:
                    lowerDepths=getArguments(string[argumentStart+1:argumentEnd], depth+1,startIndex+argumentStart+1)
                else:
                    commandName=string[start+1:end]
                print "commandName is",commandName
                expansions=dict(settingsHandler.readSettingRaw("'core-expansions'","trigger,command"))
                if commandName in (globalv.loadedPlugins.keys() + expansions.keys()):
                    positions+=lowerDepths+[(depth, startIndex+start, startIndex+end+1)]
                argumentStart=-1
                lowerDepths=[]
                argumentEnd=-1
                argumentDepth=0
                hasArguments=False
                start=-1
                end=-1
                continue
        if letter==argumentCharacter[0] and not hasArguments:
            hasArguments=True
            commandName=string[start+1:index]
            argumentStart=index
            argumentDepth+=1
        elif letter==argumentCharacter[0]:
            argumentDepth+=1
        elif letter==argumentCharacter[-1]:
            argumentDepth-=1
            if argumentDepth==0:
                argumentEnd=index
        elif letter in breakCharacters and not hasArguments:
            argumentStart=-1
            lowerDepths=[]
            argumentEnd=-1
            argumentDepth=0
            hasArguments=False
            start=-1
            end=-1
    return positions

