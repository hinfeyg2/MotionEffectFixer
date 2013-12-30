#!/usr/bin/env python
import re


rate = 25
def tc_to_frame(hh, mm, ss, ff):
    return ff + (ss + mm*60 + hh*3600) * rate

def frame_to_tc(fn):
    ff = fn % rate
    s = fn // rate
    return (s // 3600, s // 60 % 60, s % 60, ff)
    
def addleadingzero(number):

	if len(str(number)) == 1:
		return "0" + str(number)
	else:
		return str(number)  
		  
    
edlIn = open("EP2 EDLS SIMON.edl", "r+")
edlOut = open("TESTOUT.EDL", "w")
count = 0
lines = edlIn.readlines()

for line in lines:
	if str(line.isspace()):
		edlOut.write(line)
	else:
		edlOut.write("\n")
		edlOut.write(line)
	count += 1
	matchObj = re.search( r'\d\d:\d\d:\d\d:\d\d \d\d:\d\d:\d\d:\d\d \d\d:\d\d:\d\d:\d\d \d\d:\d\d:\d\d:\d\d', line, re.M|re.I)
	if matchObj:
		dogs = lines[count]
		motionM = str(dogs[0])
		foundtimecode = matchObj.group()
		EDLindexNumber = str(line)
		TimecodeInstancesList = foundtimecode.split( )
		timecodeone = TimecodeInstancesList[0]
		timecodetwo = TimecodeInstancesList[1]
		timecodethree = TimecodeInstancesList[2]
		timecodefour = TimecodeInstancesList[3]
		
		tempcodesplitone = timecodeone.split(":")
		timecodeoneframes = tc_to_frame(int(tempcodesplitone[0]), int(tempcodesplitone[1]), int(tempcodesplitone[2]), int(tempcodesplitone[3]))
		
		tempcodesplittwo = timecodetwo.split(":")
		timecodetwoframes = tc_to_frame(int(tempcodesplittwo[0]), int(tempcodesplittwo[1]), int(tempcodesplittwo[2]), int(tempcodesplittwo[3]))
		
		tempcodesplitthree = timecodethree.split(":")
		timecodethreeframes = tc_to_frame(int(tempcodesplitthree[0]), int(tempcodesplitthree[1]), int(tempcodesplitthree[2]), int(tempcodesplitthree[3]))
		
		tempcodesplitfour = timecodefour.split(":")
		timecodefourframes = tc_to_frame(int(tempcodesplitfour[0]), int(tempcodesplitfour[1]), int(tempcodesplitfour[2]), int(tempcodesplitfour[3]))
		
		sequenceframes = timecodefourframes - timecodethreeframes
		sourceframes = timecodetwoframes - timecodeoneframes
		
		splitting = line.split( )
		clipname = splitting[1]
		
		if sequenceframes != sourceframes and motionM != "M":
			percentage = (float(sourceframes) / float(sequenceframes)) * rate
			motioneffectpercent = int(percentage * 10**0) / 10**0
			if motioneffectpercent > 75:
				motioneffectpercent = 100
			else:
				motioneffectpercent = 50
			clipendtimecode = addleadingzero(tempcodesplitone[0]) + ":" + addleadingzero(tempcodesplitone[1]) + ":" + addleadingzero(tempcodesplitone[2]) + ":" + addleadingzero(tempcodesplitone[3])
			print str(EDLindexNumber[0:6]) + " is a buried Motion effect. Should be in or around a " + str(motioneffectpercent) + "fps motion effect."
			if len(str(motioneffectpercent)) < 3:
				edlOut.write("M2      " + str(clipname) + "                      " + "0" + str(motioneffectpercent) + ".0 " + str(clipendtimecode) + " ")
			elif len(str(motioneffectpercent)) >= 3:
				edlOut.write("M2      " + str(clipname) + "                      " + str(motioneffectpercent) + ".0 " + str(clipendtimecode) + " ")
			
		else:
			pass
		
		
	else:
		pass
	
