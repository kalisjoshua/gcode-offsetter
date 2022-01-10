from pathlib import Path
import re
import sys


def findContent (str,param):
    reSearch = re.compile(param+'(\d*.\d*)')
    parts = reSearch.search(str)
    return parts



def ProcessFile (filenameIn, filenameOut):
    if onlyAnalyse == False:
        fileOut = open(Path(filenameOut),'w')
        print("Writing to "+filenameOut)

    minX = LimMaxX
    maxX = 0.0
    minY = LimMaxY
    maxY = 0.0
    minZ = LimMaxZ
    maxZ = 0.0
    with open(Path(filenameIn),'r') as fileIn:
        for line in fileIn:
            linesplit = line.split()
            #check if command is a move
            if linesplit :
                if linesplit[0] == 'G0' or linesplit[0] == 'G1':
                    for parts in linesplit:
                        if parts[0:1] == ';':
                            #end of line / comment reached
                            break
                        # setup line with first command
                        if parts[0:1] == 'G':
                            lineNew = parts
                        else:
                            valuestr = findContent(parts,parts[0:1])
                            if valuestr:
                                currentPos = float(valuestr.groups()[0])
                            else:
                                currentPos = 0
                            match parts[0:1]:
                                case 'X':
                                    currentPos = Transpose(currentPos,deltaX,0,LimMaxX)
                                    lineNew+= ' '+parts[0:1]+"{:.6f}".format(currentPos)
                                    if currentPos > maxX:
                                        maxX = currentPos
                                    if currentPos < minX:
                                        minX = currentPos
                                case 'Y':
                                    currentPos = Transpose(currentPos,deltaY,0,LimMaxY)
                                    lineNew+= ' '+parts[0:1]+"{:.6f}".format(currentPos)
                                    if currentPos > maxY:
                                        maxY = currentPos
                                    if currentPos < minY:
                                        minY = currentPos
                                case 'Z':
                                    currentPos = Transpose(currentPos,deltaZ,0,LimMaxZ)
                                    lineNew+= ' '+parts[0:1]+"{:.6f}".format(currentPos)
                                    if currentPos > maxZ:
                                        maxZ = currentPos
                                    if currentPos < minZ:
                                        minZ = currentPos
                                case 'F':
                                    #TODO: add proper FRate handling
                                    currentPos = Transpose(currentPos,deltaF,0,LimMaxF)
                                    lineNew+= ' '+parts[0:1]+str(currentPos)
                                case 'E':
                                    #TODO: add proper ERate handling
                                    currentPos = Transpose(currentPos,deltaE,-LimMaxE,LimMaxE)
                                    lineNew+= ' '+parts[0:1]+str(currentPos)
                    line = lineNew+'\n'
                if onlyAnalyse == False:
                    fileOut.write(line)
        print("min X "+str(minX)+" maxX "+str(maxX)+" width "+str(maxX-minX))
        print("min Y "+str(minY)+" maxY "+str(maxY)+" width "+str(maxY-minY))
        print("min Z "+str(minZ)+" maxZ "+str(maxZ)+" width "+str(maxZ-minZ))



def Transpose (position,offset,min,max):
    position+= offset
    if position < min:
        position = min
    elif position >   max:
        position = max
    return round(position,6)

    

deltaX = 0.0
deltaY = 0.0
deltaZ = 0.0
deltaF = 0.0
deltaE = 0.0

LimMaxX = 220
LimMaxY = 220
LimMaxZ = 250
LimMaxF = 50000.0
LimMaxE = 50000.0
filenameIn = ''
filenameOut = ''
onlyAnalyse = False

for argument in sys.argv:
    keyword = argument[0:2]
    userData = argument[2:len(argument)]
    match keyword:
        case '-i':
            filenameIn = userData
        case '-o':
            filenameOut = userData
        case '-X':
            deltaX = float(userData)
        case '-Y':
            deltaY = float(userData)
        case '-Z':
            deltaZ = float(userData)
        case '-F':
            deltaF = float(userData)
        case '-E':
            deltaE = float(userData)
        case '-h':
            print('gcode_move -iInputFile -oOutputFile -Xoffset -Yoffset -Zoffset -FFeedrate -EExtruderrate')
            print('           -aAnalyseOnly')
            quit()
        case '-a':
            onlyAnalyse = True

if filenameOut == '':
    filenameOut = 'out'+filenameIn
ProcessFile(filenameIn,filenameOut)




