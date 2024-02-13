# Import Python and Maya modules
import maya.cmds
import random
import math

# Import custom modules
import utilities


ver = ' : ver 01.006 ' # This needs to be updated each time the script is updated or modified.
comment = 'Imported setUpGroups function from Utilities. Replace setUpGrp with utilities.setUpGroups in setupSplineIK02 function.'
print ("#### Imported UtilitiesRigging Module" + ver)

def getVersion():
	print ("Imported Utilities Rigging Module " + ver)


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. jointArray = TODO

OUTPUT :
1. returnArray = TODO

NOTES : 
1. NA
"""		
def addClaw(prefix,jointArray,rollLoc,jointAimAxis,jointUpAxis,ctrl):
	returnArray = []

	aimVect = getVector(jointAimAxis)
	upVect = getVector(jointUpAxis)
	pitchAxis = getPitchAxis(jointAimAxis,jointUpAxis)

	getBranchNumber = getSuffix(jointArray[1],1)

	#1. CREATE INITIAL BASE LOCATOR FIRST LOCATOR THAT IS PARENTED ON THE ANKLE JOINT AND IS AIMED AT THE TOE
	name = findName(jointArray[0],prefix)
	name = name + '_base' + getBranchNumber
	createLocator = maya.cmds.spaceLocator(n=name, p=(0,0,0))[0]
	whichJoint = jointArray[0]
	constainLocator = maya.cmds.parentConstraint(whichJoint, createLocator, weight=1 )
	maya.cmds.delete(constainLocator)
	maya.cmds.parent(createLocator,rollLoc,a=True)
	ac = maya.cmds.aimConstraint( jointArray[1],createLocator,offset=(0,0,0), weight=1, aimVector=(aimVect[0],aimVect[1],aimVect[2]), upVector=(upVect[0],upVect[1],upVect[2]), worldUpType='vector', worldUpVector=(0,1,0))
	maya.cmds.delete(ac)
	returnArray.append(createLocator)
	previousLocator = createLocator

	#2. CREATE SECONDARY LOCATOR PARENT TO THE FIRST LOCATOR. THIS WILL ACT AS A ROLL AND PITCH  LOCATOR
	#CREATE ATTRIBUTES
	name = findName(jointArray[0],prefix)
	name = name  + '_B' + getBranchNumber
	createLocator = maya.cmds.spaceLocator(n=name + '_LOC', p=(0,0,0))[0]
	whichJoint = jointArray[0]
	constainLocator = maya.cmds.parentConstraint(previousLocator, createLocator, weight=1 )
	maya.cmds.delete(constainLocator)

	#2. CONNECT SECONDARY LOCATOR TO CONTROL ATTRIBUTES
	#print('2. CONNECT :: createLocator = ' + str(createLocator))
	rotAttr = name + '_Side'
	checkAttrExist(ctrl,rotAttr,'double',-90,90,0,True,True)
	#print('rotAttrC = ' + str(rotAttr))
	maya.cmds.parent(createLocator,previousLocator,a=True)
	destination = createLocator + '.r' + jointAimAxis
	source = ctrl + '.' + rotAttr
	maya.cmds.connectAttr(source, destination, force=True)
	pitAttr = name + '_Up'
	checkAttrExist(ctrl,pitAttr,'double',-90,90,0,True,True)
	destination = createLocator + '.r' + pitchAxis
	source = ctrl + '.' + pitAttr
	maya.cmds.connectAttr(source, destination, force=True)
	returnArray.append(createLocator)
	previousLocator = createLocator

	#CREATE THIRD LOCATOR PARENT TO THE CLAW ANKLE JOINT
	name = findName(jointArray[1],prefix)
	name = name + '_Base' + getBranchNumber
	createLocator = maya.cmds.spaceLocator(n=name + '_LOC', p=(0,0,0))[0]
	whichJoint = jointArray[1]
	#POSITION FOOT LOCATOR AT FOOT JOINT, THEN PARENT THE FOOT LOCATOR TO THE ANKLE LOCATOR, MAINTAIN OFFSET
	constainLocator = maya.cmds.parentConstraint(whichJoint, createLocator, weight=1 )
	maya.cmds.delete(constainLocator)
	maya.cmds.parent(createLocator,previousLocator,a=True)
	#AIM THE FOOT LOCATOR AT THE TOE JOINT, MAKE SURE THAT FOOT LOCATORS TRANSLATE IS ONLY ON THE AIM AXIS
	ac = maya.cmds.aimConstraint( jointArray[2],createLocator,offset=(0,0,0), weight=1, aimVector=(aimVect[0],aimVect[1],aimVect[2]), upVector=(upVect[0],upVect[1],upVect[2]), worldUpType='vector', worldUpVector=(0,1,0))
	maya.cmds.delete(ac)
	constainLocator = maya.cmds.parentConstraint(createLocator, jointArray[1], weight=1, mo=True )
	previousLocator = createLocator
	returnArray.append(createLocator)

	#CREATE FOURTH LOCATOR PARENT TO THE CLAW FOOT JOINT AND CREATE SINGLE CHAIN IK AND PARENT TO NEW JOINT
	name = findName(jointArray[1],prefix)
	name = name + 'B' + getBranchNumber
	createLocator = maya.cmds.spaceLocator(n=name + '_LOC', p=(0,0,0))[0]
	constainLocator = maya.cmds.parentConstraint(previousLocator, createLocator, weight=1 )
	maya.cmds.delete(constainLocator)
	maya.cmds.parent(createLocator,previousLocator,a=True)
	toeIK = createIKhandles('',name + '_','ikSCsolver',jointArray[1],jointArray[2],False,None,None)[0]
	maya.cmds.parent(toeIK,createLocator,a=True)
	previousLocator = createLocator
	returnArray.append(createLocator)

	#ADD ATTRIBUTES TO ROLL CLAW FROM SIDE TO SIDE AND ANGLE THE TOE UP AND DOWN
	pitAttr = name + '_Up'
	checkAttrExist(ctrl,pitAttr,'double',-90,90,0,True,True)
	destination = createLocator + '.r' + pitchAxis
	source = ctrl + '.' + pitAttr
	maya.cmds.connectAttr(source, destination, force=True)

	return returnArray
	
	
"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. jointArray = TODO

OUTPUT :
1. returnArray = TODO

NOTES : 
1. NA
"""	
def createLocatorsOnJointChain(jointArray,parentLocs):
	#print('createLocatorsOnJointChain :: jointArray = ' + str(jointArray))
	returnArray = []
	#print('utilitiesRigging :: jointArray = ' + str(jointArray))
		
	for j in range(0,len(jointArray),1):
		name = jointArray[j] + '_LOC'
		createLocator = maya.cmds.spaceLocator(n=name, p=(0,0,0))[0]
		#print('utilitiesRigging :: createLocator = ' + str(createLocator))
		#print('utilitiesRigging :: jointArray[j] = ' + str(jointArray[j]))
		constrainLocator = maya.cmds.parentConstraint( jointArray[j], createLocator, weight=1 )
		maya.cmds.delete(constrainLocator)
		returnArray.append(createLocator)
		# Check to see if the joints need to be in parent chain
		if(parentLocs):
			if(j != 0):
				maya.cmds.parent(createLocator,previousLocator,a=True)

		if(j == len(jointArray)-1):
			#print('createLocatorsOnJointChain :: j = ' + str(j))
			#maya.cmds.setAttr(createLocator + '.translateX', 0)
			#maya.cmds.setAttr(createLocator + '.translateY', 0)
			#maya.cmds.setAttr(createLocator + '.translateZ', 0)
			maya.cmds.setAttr(createLocator + '.rotateX', 0)
			maya.cmds.setAttr(createLocator + '.rotateY', 0)
			maya.cmds.setAttr(createLocator + '.rotateZ', 0)
		
		previousLocator = createLocator

	return returnArray


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. jointArray = TODO
2. sidePrefix = TODO
3. jointType = TODO
4. groupArray = TODO

OUTPUT :
1. newArray = TODO

NOTES : 
1. NA
"""	
# Formerly known as copySelectedJoints
def duplicateSelectedJoints(jointArray,sidePrefix,jointType,groupArray):
	prefix = sidePrefix + jointType
	newArray = []
	#print('createIKjoints :: jointArray = ' + str(jointArray))
	maya.cmds.select( clear=True )
	duplicateJoint = maya.cmds.duplicate(jointArray[0])[0]
	n = findNamePrefix(jointArray[0],sidePrefix)
	j = maya.cmds.rename(duplicateJoint,prefix + n)
	newArray.append(j)

	allChildren = maya.cmds.listRelatives(j,ad=True,f=True)
	
	#DELETE UNWANTED JOINTS
	for c in allChildren:
		prefixToIgnore = c.rfind('|')
		n = c[prefixToIgnore+1:len(c)]
		delete = True
		for i in range(1,len(jointArray),1):
			#print('createIKjoints :: compare ' + str(n) + ' : ' + str(jointArray[i]))
			if(n == jointArray[i]):
				delete = False

		if(delete == True):
			maya.cmds.delete(c)
		else:
			maya.cmds.rename(c,prefix + n)

	allChildren = maya.cmds.listRelatives(j,ad=True,f=True)
	revAllChildren = reverseArray(allChildren)
	#print('createIKjoints :: revAllChildren = ' + str(revAllChildren))
	for c in revAllChildren:
		newArray.append(c)

	#print('createIKjoints :: newArray = ' + str(newArray))

	maya.cmds.parent(newArray[0],groupArray[len(groupArray)-1])
	return newArray



"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. curve = TODO
2. nme = TODO
3. grp = TODO

OUTPUT :
1. listOfClusters = TODO
2. returnCV = TODO

NOTES : 
1. NA
"""	
# formerly known as clusterCurve
def createClusterCurve(curve,nme,grp):
	returnCV = []
	maya.cmds.select(curve + '.cv[*]')
	cvs = maya.cmds.ls(selection=True)
	#print ('cvs = ' + str(cvs))
	#print('cvs length = ' + str(len(cvs)))
	rf = cvs[0].rfind(':')
	#print ('rf = ' + str(rf))
	lenCVs = len(cvs[0])
	#print ('lenCVs = ' + str(lenCVs))
	number = int(cvs[0][(rf+1):(lenCVs-1)])
	cvName = cvs[0][0:rf-2]
	#print ('number = ' + str(number))
	#print ('cvName = ' + str(cvName))
	
	listOfClusters = []
	for i in range(0,number+1,1):
		returnCV.append(str(cvName) + '[' + str(i) + ']')
		#print ('clusterCurve : returnCV = ' + str(returnCV))
		c = maya.cmds.cluster(str(curve) + '.cv[' + str(i) + ']')
		nn = maya.cmds.rename(c[1],nme+str(i+1))
		listOfClusters.append(nn)
		if( grp != None ):
			maya.cmds.parent(nn,grp)

	#print ('listOfClusters = ' + str(listOfClusters))
	return (listOfClusters,returnCV)


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. jointArray = TODO
2. sidePrefix = TODO
3. jointType = TODO
4. groupArray = TODO

OUTPUT :
1. newArray = TODO

NOTES : 
1. NA
"""	
def createIKjoints(jointArray,sidePrefix,jointType,groupArray):
	newArray = []
	#brake = False
	#print('createIKjoints :: jointArray = ' + str(jointArray))
	endJoint = jointArray[len(jointArray)-1]
	#print('createIKjoints :: endJoint = ' + str(endJoint))
	maya.cmds.select( clear=True )
	duplicateJoint = maya.cmds.duplicate(jointArray[0])[0]
	maya.cmds.makeIdentity( duplicateJoint, apply=True, t=0, r=1, s=0, n=0 )
	maya.cmds.parent(duplicateJoint, w=True)
	howManyJoints = len(jointArray)
	for i in range(0,len(jointArray),1):
		n = findNamePrefix(jointArray[i],sidePrefix)
		newn = sidePrefix + jointType + n
		#print('createIKjoints :: newn = ' + str(newn))
		#print('createIKjoints :: duplicateJoint = ' + str(duplicateJoint))
		j = maya.cmds.rename(duplicateJoint,newn)
		newArray.append(j)
		child = maya.cmds.listRelatives(j,c=True,f=True)
		#print('createIKjoints :: child = ' + str(duplicateJoint))
		if(child != None):
			if(len(child) == 1):
				duplicateJoint = child[0]
			else:
				#print('createIKjoints :: child = ' + str(child))
				#print('createIKjoints :: ' + str(j) + ' has a branch of Multiple Joints')
				for c in child:
					#print('createIKjoints :: c = ' + str(c))
					gc = maya.cmds.listRelatives(c,c=True,ad=True,f=True)
					#print('createIKjoints :: gc = ' + str(gc))
					if(gc != None):
						for g in gc:
							prefixToIgnore = g.rfind('|')
							test = g[prefixToIgnore+1:len(g)]
							#print('createIKjoints :: test = ' + str(test))
							#print('createIKjoints :: endJoint = ' + str(endJoint))
							if(test == endJoint):
								#print('createIKjoints :: c has the end joint = ' + str(c))
								duplicateJoint = c
								#print('createIKjoints :: duplicateJoint = ' + str(duplicateJoint))
					else:	
						#print('createIKjoints :: deleting ' + str(c))
						maya.cmds.delete(c)
						duplicateJoint = maya.cmds.listRelatives(j,c=True,ad=True,f=True)[0]

	last = newArray[len(newArray)-1]
	c = maya.cmds.listRelatives(last,c=True,f=True)
	if(c != None):
		for n in c:
			maya.cmds.delete(n)
	maya.cmds.parent(newArray[0],groupArray[len(groupArray)-1])
	return newArray

	
"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. prefix = TODO
2. limbType = TODO
3. type = TODO
4. startJoint = TODO
5. endJoint = TODO
6. pvCtrl = TODO
7. curve = TODO
8. grp = TODO

OUTPUT :
1. newArray = TODO

NOTES : 
1. NA
"""	
def createIKhandles(prefix,limbType,type,startJoint,endJoint,pvCtrl,curve,grp):
	ikh = prefix + limbType + 'ikHandle'
	if(type != 'ikSplineSolver'):
		h = maya.cmds.ikHandle(n = ikh, sj = startJoint, ee = endJoint, sol = type)
		print('h = ' + str(h))
		if(type == 'ikRPsolver'):
			maya.cmds.poleVectorConstraint( pvCtrl, ikh )
	else:
		h = maya.cmds.ikHandle(n = ikh, sj = startJoint, ee = endJoint, sol = type, ccv = False, pcv = False, c = curve)[0]
		print('h = ' + str(h))
		print('createIKhandles :: grp = ' + str(grp) )
		maya.cmds.parent(h[0],grp)
				
	return h
	

"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. jointArray = TODO
2. sidePrefix = TODO
3. jointType = TODO
4. groupArray = TODO

OUTPUT :
1. newArray = TODO

NOTES : 
1. NA
"""	
# Formerly known as copySelectedJoints
def duplicateSelectedJoints(jointArray,sidePrefix,jointType,groupArray):
	prefix = sidePrefix + jointType
	newArray = []
	maya.cmds.select( clear=True )
	duplicateJoint = maya.cmds.duplicate(jointArray[0])[0]
	n = findNamePrefix(jointArray[0],sidePrefix)
	j = maya.cmds.rename(duplicateJoint,prefix + n)
	newArray.append(j)

	allChildren = maya.cmds.listRelatives(j,ad=True,f=True)
	
	#DELETE UNWANTED JOINTS
	for c in allChildren:
		prefixToIgnore = c.rfind('|')
		n = c[prefixToIgnore+1:len(c)]
		delete = True
		for i in range(1,len(jointArray),1):
			if(n == jointArray[i]):
				delete = False

		if(delete == True):
			maya.cmds.delete(c)
		else:
			maya.cmds.rename(c,prefix + n)

	allChildren = maya.cmds.listRelatives(j,ad=True,f=True)
	revAllChildren = reverseArray(allChildren)
	for c in revAllChildren:
		newArray.append(c)

	maya.cmds.parent(newArray[0],groupArray[len(groupArray)-1])
	return newArray
	
	
"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. jointArray = String Array
2. obj = String

OUTPUT :
1. returnArray = String Array

NOTES : 
1. NA
"""	
def duplicatedSelectedOnJointChain(jointArray,obj):
	returnArray = []
	previousObj = jointArray[0] + '_CTRL'
	
	for j in range(0,len(jointArray),1):
		name = jointArray[j] + '_CTRL'
		currentObj = maya.cmds.duplicate(obj,n=name)[0]
		#print('duplicatedSelectedOnJointChain :: currentObj = ' + str(currentObj))
		constainLocator = maya.cmds.parentConstraint(jointArray[j], currentObj, weight=1 )
		maya.cmds.delete(constainLocator)
		returnArray.append(currentObj)
		if(j > 0):
			maya.cmds.parent(currentObj,previousObj,a=True)
		
		previousObj = currentObj

	return returnArray
	

"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. curve = TODO

OUTPUT :
1. returnCV = TODO

NOTES : 
1. NA
"""		
def getCVlist(curve):
	returnCV = []
	maya.cmds.select(curve + '.cv[*]')
	cvs = maya.cmds.ls(selection=True)
	#print ('cvs = ' + str(cvs))
	#print('cvs length = ' + str(len(cvs)))
	rf = cvs[0].rfind(':')
	#print ('rf = ' + str(rf))
	lenCVs = len(cvs[0])
	#print ('lenCVs = ' + str(lenCVs))
	number = int(cvs[0][(rf+1):(lenCVs-1)])
	cvName = cvs[0][0:rf-2]
	#print ('number = ' + str(number))
	#print ('cvName = ' + str(cvName))
	
	listOfClusters = []
	for i in range(0,number+1,1):
		returnCV.append(str(cvName) + '[' + str(i) + ']')

	#print ('returnCV = ' + str(returnCV))
	return returnCV


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. jointArray = Array String
2. howManyTweenJoints = Integer

OUTPUT :
1. newArray = Array String

NOTES : 
1. NA
"""	
def getTweenJoints(jointArray,howManyTweenJoints):
	increment = 0
	newArray = []
	#print('getTweenJoints :: increment = ' + str(increment) )
	#print('jointArray = ' + str(jointArray) )
	for j in range(0,len(jointArray),1):
		print('getTweenJoints :: j = ' + str(j) )
		if( j == increment ):
			increment = increment + howManyTweenJoints + 1
			#print('getTweenJoints :: increment = ' + str(increment) )
		else:
			newArray.append(jointArray[j])
			#print('getTweenJoints :: newArray = ' + str(newArray) )

	return newArray

	
"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. selectedObj = String
2. type = String

OUTPUT :
1. newArray = Array String

NOTES : 
1. NA
"""	
def getTweenJointsAuto(selectedObj,type):
	newArray = []
	
	for i in range(1,len(selectedObj),1):
		list = maya.cmds.listRelatives(selectedObj[i-1],ad=True,typ=type)
		reverseList = reverseArray(list)
		selection = filterSelection2(reverseList,selectedObj[i],1)
		for j in range(0,len(selection)-1,1):
			newArray.append(selection[j])

	print('getTweenJoints :: newArray = ' + str(newArray))

	return newArray


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. howManyTweenJoints = Integer
2. howManySplineIKControlJoints = String Array
3. tweenSplineJoints = String Array
4. jointAimAxis = String

OUTPUT :
1. tsj = TODO
2. multiplier = TODO

NOTES : 
1. NA
"""		
# Formerly known as insertHowManySplineIKJoints
def insertSplineIKJoints(howManyTweenJoints,howManySplineIKControlJoints,tweenSplineJoints):
	tsj = tweenSplineJoints * (howManySplineIKControlJoints + 1)
	#print('cj = ' + str(cj))
	#tsj = (cj+1) * tweenSplineJoints
	#print('tsj = ' + str(tsj))
	#print('tweenSplineJoints = ' + str(tweenSplineJoints))
	multiplier = tweenSplineJoints + 1
	if(howManySplineIKControlJoints == 0):
		multiplier = 0
	if(tweenSplineJoints == 0):
		#tweenSplineJoints = 1
		tsj = tweenSplineJoints + howManySplineIKControlJoints
		multiplier = 1
	#print('multiplier = ' + str(multiplier))
	return (tsj,multiplier)


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. selectedJoints = String Array
2. jointTypePrefix = String
3. sidePrefix = String
4. jointAimAxis = String
5. howManyTweenJoints = Integer

OUTPUT :
1. jointsInserted = Array String
2. alljoints = TODO

NOTES : 
1. NA
"""	
def insertExtraJoints(selectedJoints,jointTypePrefix,sidePrefix,jointAimAxis,howManyTweenJoints):
	#print('insertExtraJoints00 :: selectedJoints = ' + str(selectedJoints))
	maya.cmds.select( clear=True )
	oldMasterJoints = []
	howManySelJoints = len(selectedJoints)
	alljoints = []
	jointsInserted = []
	#print('insertExtraJoints00 :: howManySelJoints = ' + str(howManySelJoints))
	for i in range(0,howManySelJoints-1,1):
		#print('insertExtraJoints00 :: i = ' + str(i))
		masterJoint = selectedJoints[i]
		alljoints.append(masterJoint)
		#print('insertExtraJoints00 :: masterJoint = ' + str(masterJoint))
		#print('insertExtraJoints00 :: selectedJoints[i] = ' + str(selectedJoints[i]))
		t = maya.cmds.rename(selectedJoints[i],'temp_' + masterJoint)
		oldMasterJoints.append(t)
		#print('insertExtraJoints00 :: oldMasterJoints = ' + str(oldMasterJoints))
		getOldMasterJointPos = getWStransform(oldMasterJoints[i])
		masterJointName = findName(masterJoint,sidePrefix)
		translateAxis = '.t' + jointAimAxis
		jointDistance = getDistance2Vectors(oldMasterJoints[i],selectedJoints[i+1])
		jointTweendistance = jointDistance / (howManyTweenJoints + 1)
		getMasterJointPos = getWStransform(oldMasterJoints[i])
		previousJoint = maya.cmds.joint( n=masterJoint)

		for j in range(1,howManyTweenJoints+1,1):
			v = incrementPos(jointTweendistance,(j-1)*jointTweendistance,jointAimAxis)
			previousJoint = maya.cmds.joint( previousJoint,n=sidePrefix + jointTypePrefix[i] + str(j), p=v )
			alljoints.append(previousJoint)
			jointsInserted.append(previousJoint)

		setWStransform(masterJoint,getOldMasterJointPos)

		if(jointAimAxis == 'x'):
			aim = maya.cmds.aimConstraint( str(selectedJoints[i+1]), masterJoint, aimVector=(1,0,0), skip=["x"] )
			maya.cmds.delete(aim)
		elif(jointAimAxis == 'y'):
			aim = maya.cmds.aimConstraint( str(selectedJoints[i+1]), masterJoint, aimVector=(0,1,0), skip=["y"] )
			maya.cmds.delete(aim)
		else:
			aim = maya.cmds.aimConstraint( str(selectedJoints[i+1]), masterJoint, aimVector=(0,0,1), skip=["z"] )
			maya.cmds.delete(aim)
	
		setJointOriention(masterJoint)
		parent = maya.cmds.listRelatives( oldMasterJoints[i], parent=True )
		#print('insertExtraJoints00 :: parent = ' + str(parent))
		if(parent != None):
			maya.cmds.parent(masterJoint,parent[0])
		
		maya.cmds.parent(selectedJoints[i+1],previousJoint)
		maya.cmds.delete(oldMasterJoints[i])
		maya.cmds.select( clear=True )

	alljoints.append(selectedJoints[howManySelJoints-1])
	#print('insertExtraJoints00 :: alljoints = ' + str(alljoints))
	#print('insertExtraJoints00 :: jointsInserted = ' + str(jointsInserted))
	return(jointsInserted,alljoints)


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. jointArray = String Array
2. howManyJointsInserted = Integer
3. sidePrefix = String
4. prefix = String
5. suffix = String
6. jointAimAxis = TODO

OUTPUT :
1. jointsInserted = Array String
2. alljoints = TODO

NOTES : 
1. NA
"""
def insertExtraJoints02(jointArray,howManyJointsInserted,sidePrefix,prefix,suffix,jointAimAxis):
	jointsInserted = []
	allJoints = []
	#print('insertExtraJoints06 :: howManyJointsInserted = ' + str(howManyJointsInserted))
	#print('insertExtraJoints06 :: jointArray = ' + str(jointArray))
	
	howManyJoints = len(jointArray)
	jointRadius = maya.cmds.getAttr(jointArray[0] + '.radius')

	PosOrNeg = 1

	if(sidePrefix == 'L_'):
		PosOrNeg = 1
		#print('LEFT')
	else:
		PosOrNeg = 1
		#print("RIGHT")

	#create the controls
	for i in range(0, howManyJoints-1, 1):
		
		increment = 1
		nextIndex = i + 1
		nextJoint = jointArray[nextIndex]
		#print('insertExtraJoints06 :: nextJoint = ' + str(nextJoint))
		currentJoint = jointArray[i]
		#print('insertExtraJoints06 :: currentJoint = ' + str(currentJoint))
		previousJoint = jointArray[i]
		#print('insertExtraJoints06 :: previousJoint = ' + str(previousJoint))
		translate = maya.cmds.getAttr(nextJoint  + '.t' + jointAimAxis)
		jointSpacing = PosOrNeg * (translate / (howManyJointsInserted+1))
		#print('insertExtraJoints06 :: jointSpacing = ' + str(jointSpacing))
		allJoints.append(currentJoint)
		#print('insertExtraJoints06 :: allJoints = ' + str(allJoints))
		for j in range(0,howManyJointsInserted,1):
			#print('insertExtraJoints06 :: j = ' + str(j))
			insertJoint = maya.cmds.insertJoint(previousJoint)
			createJoint = maya.cmds.rename(insertJoint,prefix + jointArray[i] + '_' + str(increment)  + suffix)
			jointsInserted.append(createJoint)
			#print('insertExtraJoints06 :: jointsInserted = ' + str(jointsInserted))
			allJoints.append(createJoint)
			#print('insertExtraJoints06 :: allJoints = ' + str(allJoints))
			maya.cmds.setAttr (createJoint + '.t' + jointAimAxis,jointSpacing)
			maya.cmds.setAttr (createJoint + '.radius', jointRadius)
			previousJoint = createJoint
			#print('insertExtraJoints06 :: previousJoint = ' + str(previousJoint))
			increment = increment + 1

		maya.cmds.setAttr (nextJoint + '.t' + jointAimAxis,jointSpacing)
		#print ('insertExtraJoints06 :: jointsInserted = ' + str(jointsInserted))
		increment = 1

	allJoints.append(nextJoint)
	#print('insertExtraJoints06 :: jointsInserted = ' + str(jointsInserted))
	#print('insertExtraJoints06 :: allJoints = ' + str(allJoints))
	return (jointsInserted,allJoints)


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. jointArray = String Array
2. howManyJointsInserted = Integer
3. sidePrefix = String
4. prefix = String
5. suffix = String
6. jointAimAxis = TODO

OUTPUT :
1. jointsInserted = Array String
2. alljoints = TODO

NOTES : 
1. NA
"""	
def insertExtraJoints03(jointArray,tweenJointArray,howManyJointsInserted,sidePrefix,prefix,suffix,jointAimAxis):
	jointsInserted = []
	allJoints = []
	#print('insertExtraJoints07 :: howManyJointsInserted = ' + str(howManyJointsInserted))
	#print('insertExtraJoints07 :: jointArray = ' + str(jointArray))
	
	howManyJoints = len(jointArray)
	jointRadius = maya.cmds.getAttr(jointArray[0] + '.radius')

	if(len(tweenJointArray) > 0):
		tweenJointArray = getTweenJointArray(jointArray,tweenJointArray)

	PosOrNeg = 1

	if(sidePrefix == 'L_'):
		PosOrNeg = 1
		#print('LEFT')
	else:
		PosOrNeg = 1
		#print("RIGHT")

	#create the controls
	for i in range(0, howManyJoints-1, 1):
		
		increment = 1
		nextIndex = i + 1
		nextJoint = jointArray[nextIndex]
		#print('insertExtraJoints07 :: nextJoint = ' + str(nextJoint))
		currentJoint = jointArray[i]
		#print('insertExtraJoints07 :: currentJoint = ' + str(currentJoint))
		previousJoint = jointArray[i]
		#print('insertExtraJoints07 :: previousJoint = ' + str(previousJoint))
		translate = maya.cmds.getAttr(nextJoint  + '.t' + jointAimAxis)
		jointSpacing = PosOrNeg * (translate / (howManyJointsInserted+1))
		#print('insertExtraJoints07 :: jointSpacing = ' + str(jointSpacing))
		allJoints.append(currentJoint)
		#print('insertExtraJoints07 :: allJoints = ' + str(allJoints))
		for j in range(0,howManyJointsInserted,1):
			#print('insertExtraJoints07 :: j = ' + str(j))
			insertJoint = maya.cmds.insertJoint(previousJoint)
			tempName = jointArray[i]
			if(len(tweenJointArray) > 0):
				if(len(tweenJointArray) > 1):
					tempName = tweenJointArray[i]
				else:
					tempName = tweenJointArray[0]
			createJoint = maya.cmds.rename(insertJoint,prefix + tempName + '_' + str(increment)  + suffix)
			jointsInserted.append(createJoint)
			#print('insertExtraJoints07 :: jointsInserted = ' + str(jointsInserted))
			allJoints.append(createJoint)
			#print('insertExtraJoints07 :: allJoints = ' + str(allJoints))
			maya.cmds.setAttr (createJoint + '.t' + jointAimAxis,jointSpacing)
			maya.cmds.setAttr (createJoint + '.radius', jointRadius)
			previousJoint = createJoint
			#print('insertExtraJoints07 :: previousJoint = ' + str(previousJoint))
			increment = increment + 1

		maya.cmds.setAttr (nextJoint + '.t' + jointAimAxis,jointSpacing)
		#print ('insertExtraJoints07 :: jointsInserted = ' + str(jointsInserted))
		increment = 1

	allJoints.append(nextJoint)
	#print('insertExtraJoints07 :: jointsInserted = ' + str(jointsInserted))
	#print('insertExtraJoints07 :: allJoints = ' + str(allJoints))
	return (jointsInserted,allJoints)

	
"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. selectedJoint = TODO
2. obj = TODO
3. jointAimAxis = TODO

OUTPUT :
1. newArray = TODO

NOTES : 
1. NA
"""	
# Formerly known as aimControlsToJoints
def setAimControlsToJoints(selectedJoint,obj,jointAimAxis):
	maya.cmds.parent(obj,selectedJoint,a=True)
	maya.cmds.setAttr(obj + '.rx', 0 )
	maya.cmds.setAttr(obj + '.ry', 90 )
	maya.cmds.setAttr(obj + '.rz', 0 )
	maya.cmds.parent(obj,w=True,a=True)

	
"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. array = TODO
2. object = TODO
3. axis = TODO

OUTPUT :
1. NA

NOTES : 
1. NA
"""	
def setConnectScaleToTranslate(array,object,axis):
	howManyMultiplyNodes = 1
	howManyObjects = len(array)
	brk = 0
	scaleAxis = 't'+ axis
	transAxis = 't'+ axis


	if(howManyObjects>3):
		howManyMultiplyNodes = int(math.ceil(float(howManyObjects) / float(3)))

	increment = 0
	whichAxis = ['X','Y','Z']

	for i in range(0, howManyMultiplyNodes, 1):
		source = object + '.' + scaleAxis #'sx'
		
		mn = maya.cmds.shadingNode('multiplyDivide', n='scaler' + str(i), au=True)
		print(howManyObjects)
		destination = mn + '.' + 'input1X'
		maya.cmds.connectAttr(source, destination, force=True)
		destination = mn + '.' + 'input1Y'
		maya.cmds.connectAttr(source, destination, force=True)
		destination = mn + '.' + 'input1Z'
		maya.cmds.connectAttr(source, destination, force=True)
		
		
		for j in range(0, 3, 1):
			if(brk==0):
				t = maya.cmds.getAttr(array[increment] + '.' + transAxis) #'tx'
				#print(howManyObjects)
				maya.cmds.setAttr(mn + '.' + 'input2' + whichAxis[j],t)
				source = mn + '.' + 'output' + whichAxis[j]
				destination = array[increment] + '.' + transAxis #'tx'
				maya.cmds.connectAttr(source, destination, force=True)
			
				increment += 1
				if(increment>len(array)):
					brk = 1


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. contraintType = TODO
2. source = TODO
3. destination = TODO
4. offset = TODO
5. name = TODO

OUTPUT :
1. constraint[0] = TODO
2. type = TODO

NOTES : 
1. NA
"""	
def setConstraint(contraintType, source, destination, offset, name):
	constraint = None
	type = 'point'
	if(contraintType == 'parent'):
		type = 'parent'
		if(name != None):
			constraint = maya.cmds.parentConstraint(source,destination, mo=offset, name = name)
		else:
			constraint = maya.cmds.parentConstraint(source,destination, mo=offset)
	elif(contraintType == 'point'):
		if(name != None):
			constraint = maya.cmds.pointConstraint(source,destination, mo=offset, name = name)
		else:
			constraint = maya.cmds.pointConstraint(source,destination, mo=offset)
	elif(contraintType == 'orient'):
		if(name != None):
			constraint = maya.cmds.orientConstraint(source,destination, mo=offset, name = name)
		else:
			constraint = maya.cmds.orientConstraint(source,destination, mo=offset)
	else:
		if(name != None):
			constraint = maya.cmds.aimConstraint(source,destination, mo=offset, name = name)
		else:
			constraint = maya.cmds.aimConstraint(source,destination, mo=offset)

	return (constraint[0],type)	
	

"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. obj = TODO

OUTPUT :
1. NA

NOTES : 
1. NA
"""	
def setJointOriention(obj):
	rx = maya.cmds.getAttr(str(obj) + '.rotateX')
	#print('rx = ' + str(rx))
	maya.cmds.setAttr(str(obj) + '.jointOrientX', rx)
	ry = maya.cmds.getAttr(str(obj) + '.rotateY')
	#print('ry = ' + str(ry))
	maya.cmds.setAttr(str(obj) + '.jointOrientY', ry)
	rz = maya.cmds.getAttr(str(obj) + '.rotateZ')
	#print('rz = ' + str(rz))
	maya.cmds.setAttr(str(obj) + '.jointOrientZ', rz)
	maya.cmds.setAttr(str(obj) + '.rotateX', 0)
	maya.cmds.setAttr(str(obj) + '.rotateY', 0)
	maya.cmds.setAttr(str(obj) + '.rotateZ', 0)

	
"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. prefix = String
2. ikHandle = String
3. pv = String

OUTPUT :
1. multiply = TODO

NOTES : 
1. Outputs the name of the Maya Multiply Utility node
"""	
def setReversePolveVector(prefix,ikHandle,pv):
	axis = ['x','y','z']
	capitalAxis = ['X','Y','Z']
	
	multiply = maya.cmds.shadingNode('multiplyDivide',n=prefix + 'reverePV_multiplyDivide' + '1',au=True)
	for a in range(0,len(axis),1):
		source =  pv + '.' + 'constraintTranslate' + capitalAxis[a]
		desitination = multiply + '.' + 'input1' + capitalAxis[a]
		maya.cmds.connectAttr(source, desitination, force=True)
		maya.cmds.setAttr(multiply + '.' + 'input2' + capitalAxis[a],-1)

		source =  multiply + '.' + 'output' + capitalAxis[a]
		desitination = ikHandle + '.' + 'poleVector' + capitalAxis[a]
		maya.cmds.connectAttr(source, desitination, force=True)

	return multiply
	

"""
USAGE :  TODO

REQUIRES:
1. utilities.checkAttrExist

INPUTS :
1. cntrl = TODO
2. parentObjArray = TODO
3. cntrlGrpName = TODO

OUTPUT :
1. multiply = TODO

NOTES : 
1. Outputs the name of the Maya Multiply Utility node
"""	
def setupControlIsolation(cntrl,parentObjArray,cntrlGrpName):
	grp = ''
	attrName = 'isolate'
	getParent = maya.cmds.listRelatives(cntrl,p=True,typ='transform')
	if(getParent != None):
		if(len(getParent) == 1):
			if(getParent[0] == cntrlGrpName):
				grp = cntrlGrpName
			else:
				grp = maya.cmds.group(em=True,n=cntrlGrpName)
				maya.cmds.parent(grp,getParent[0],r=True)
				maya.cmds.parent(cntrl,grp,r=True)
				#print grp

	else:
		grp = maya.cmds.group(em=True,n=cntrlGrpName)
		maya.cmds.parent(cntrl,grp,r=True)
		#print grp

	utilities.checkAttrExist(cntrl,attrName,'double',0,10,0,True,True)

	setRangeNode = cntrl + 'isolate_setRange'
	if(maya.cmds.objExists(setRangeNode) == False):
		setRangeNode = maya.cmds.shadingNode('setRange',n=cntrl + 'isolate_setRange',au=True)

	destination =  setRangeNode + '.valueX'
	source = cntrl + '.' + attrName
	maya.cmds.connectAttr(source, destination, force=True)
	maya.cmds.setAttr(setRangeNode + '.oldMaxX',10)
	maya.cmds.setAttr(setRangeNode + '.maxX',0)
	maya.cmds.setAttr(setRangeNode + '.oldMinX',0)
	maya.cmds.setAttr(setRangeNode + '.minX',1)

	pc = []
	for o in parentObjArray:
		pc = maya.cmds.parentConstraint(o,grp,mo=True)[0]
	attr = maya.cmds.listAttr( pc )
	conn = None
	#proceed = True
	for j in range(0,len(parentObjArray),1):
		for i in range(len(attr)-1,0,-1):
			conn = findNameFromContext(attr[i],'W' + str(j))
			#print ('conn = ' + str(conn))
			if(conn != None):
				break

		if(conn == None):
			print ('ERROR :: setUpControlIsolation :: conn = ' + str(conn) + ' No connection made pn parent constraint')
			#proceed = False
		
		else:	
			destination = pc + '.' + conn
			#print('setUpIKFKswitch :: destination = ' + str(destination))
			source =  setRangeNode + '.outValueX'
			maya.cmds.connectAttr(source, destination, force=True)

	
"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. driverArray = String Array
2. selectArray = String Array
3. constraintType = String
4. offset = TODO

OUTPUT :
1. returnArray = String Array

NOTES : 
1. NA
"""
# Formerly known as constrainSelection
def setupConstrainSelection(driverArray,selectArray,constraintType,offset):
	returnArray = []
	
	for i in range(0,len(selectArray),1):
		if((testNodeType(driverArray[i],'transform') != True) and (testNodeType(driverArray[i],'joint') != True)):
			#print ('constrainSelection :: driverArray[i]  = ' + str(driverArray[i]) )
			driverArray[i] = maya.cmds.listRelatives( driverArray[i], parent=True )[0]
			#print ('constrainSelection :: driverArray[i]  = ' + str(driverArray[i]) )

		if((testNodeType(selectArray[i],'transform') != True) and (testNodeType(selectArray[i],'joint') != True)):
			#print ('constrainSelection :: selectArray[i]  = ' + str(selectArray[i]) )
			selectArray[i] = maya.cmds.listRelatives( selectArray[i], parent=True )[0]
			#print ('constrainSelection :: selectArray[i]  = ' + str(selectArray[i]) )


		temp = setConstraint(constraintType, driverArray[i], selectArray[i], offset, None)
		#print ('constrainSelection :: temp = ' + str(temp) )

	return returnArray

	
"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. prefix = String
2. array = String Array
3. attr = String
4. axis = TODO
5. driver = String
6. driverAttr = TODO


OUTPUT :
1. nodes = String Array

NOTES : 
1. NA
"""	
#NEED TO CHANGE for i in range(0,len(array)-1,1):  Formerly known as connectFKstretch
def setupFKstretch(prefix,array,attr,axis,driver,driverAttr):
	whichAxis = ['X', 'Y', 'Z']
	brk = 0
	index = 0
	length = len(array)-1
	
	nodes = []
	
	for i in range(0,length,1):
		node = maya.cmds.shadingNode('multiplyDivide',n=prefix + 'stretch_multiplyDivide' + str(i),au=True)
		nodes.append(node)
		for j in range(0,3,1):
			if(brk == 0):
				value = maya.cmds.getAttr(array[index]  + '.' + attr + axis)
				print (value)
				maya.cmds.setAttr(nodes[i]  + '.' + 'input2' + whichAxis[j], value)

				source =  driver + '.' + driverAttr
				desitination = nodes[i] + '.' + 'input1' + whichAxis[j]
				maya.cmds.connectAttr(source, desitination, force=True)

				source =  nodes[i] + '.output' + whichAxis[j]
				desitination = array[index]  + '.' + attr + axis
				maya.cmds.connectAttr(source, desitination, force=True)
				
				if(index == length):
					brk = 1
					
				index = index + 1

	return nodes
	

"""
USAGE :  TODO

REQUIRES:
1. utilities.checkAttrExist

INPUTS :
1. prefix = String
2. mainCTRL = String
3. stretchIKAttr = String
5. multiplyNode = TODO
6. curveInfoNode = TODO

OUTPUT :
1. NA

NOTES : 
1. NA
""" 
def setupSplineIkStretchAttr(prefix, mainCTRL,stretchIKAttr,multiplyNode,curveInfoNode):
	utilities.checkAttrExist(mainCTRL,stretchIKAttr,'double',0,10,0,True,True)
	setRangeNode = maya.cmds.shadingNode('setRange',n=prefix + stretchIKAttr + '_setRange',au=True)
	destination = setRangeNode + '.valueX'
	source = mainCTRL + '.' + stretchIKAttr
	maya.cmds.connectAttr(source, destination, force=True)

	utilities.checkAttrExist(mainCTRL,stretchIKAttr + '_crvinfo','double',-1000,1000,0,False,True)
	al = maya.cmds.getAttr(curveInfoNode + '.arcLength')
	maya.cmds.setAttr(mainCTRL + '.' + stretchIKAttr + '_crvinfo', al )

	destination = setRangeNode + '.valueY'
	source = mainCTRL + '.' + stretchIKAttr
	maya.cmds.connectAttr(source, destination, force=True)

	maya.cmds.setAttr(setRangeNode + '.oldMaxX', 10)
	maya.cmds.setAttr(setRangeNode + '.maxX', 1)
	maya.cmds.setAttr(setRangeNode + '.oldMinX', 0)
	maya.cmds.setAttr(setRangeNode + '.minX', 0)

	StretchBlendNode = maya.cmds.shadingNode('blendColors',n=prefix + stretchIKAttr + '_blend',au=True)
	destination =  StretchBlendNode + '.color1R'
	source =  mainCTRL + '.' + stretchIKAttr + '_crvinfo'
	maya.cmds.connectAttr(source, destination, force=True)

	destination =  StretchBlendNode + '.color2R'
	source =  curveInfoNode + '.arcLength'
	maya.cmds.connectAttr(source, destination, force=True)

	destination =  multiplyNode + '.input2X'
	source =  StretchBlendNode + '.outputR'
	maya.cmds.connectAttr(source, destination, force=True)

	destination =  StretchBlendNode + '.blender'
	source =  setRangeNode + '.outValueX'
	maya.cmds.connectAttr(source, destination, force=True)

	maya.cmds.setAttr(mainCTRL + '.' + stretchIKAttr + '_crvinfo', lock = True, keyable = False, channelBox = False)
	
	
"""
USAGE :  TODO

REQUIRES:
1. utilities.checkAttrExist

INPUTS :
1. prefix = String
2. array = String Array
3. ctrl = String
5. ik = TODO
6. fk = TODO

OUTPUT :
1. setRangeNode = String

NOTES : 
1. NA
""" 
def setUpIKFKswitch(prefix,array,ctrl,ik,fk):
	utilities.checkAttrExist(ctrl,'IkFk','double',0,10,0,True,False)
	#print('setUpIKFKswitch :: prefix = ' + str(prefix))
	#print('setUpIKFKswitch :: array = ' + str(array))
	#print('setUpIKFKswitch :: ctrl = ' + str(ctrl))
	setRangeNode = prefix + 'IKFK_setRange'
	if(maya.cmds.objExists(setRangeNode) == False):
		setRangeNode = maya.cmds.shadingNode('setRange',n=prefix + 'IKFK_setRange',au=True)

	destination =  setRangeNode + '.valueX'
	source =  ctrl + '.IkFk'
	testConnection = maya.cmds.isConnected( source, destination )
	if(testConnection == 0):
		maya.cmds.connectAttr(source, destination, force=True)
	
	destination =  setRangeNode + '.valueY'
	testConnection = maya.cmds.isConnected( source, destination )
	if(testConnection == 0):
		maya.cmds.connectAttr(source, destination, force=True)
	
	for c in array:
		if(c != None):
			#print('setUpIKFKswitch :: c[0] = ' + str(c[0]))
			attr = maya.cmds.listAttr( c[0] )
			#print('setUpIKFKswitch :: attr = ' + str(attr))
			conn1 = None
			conn2 = None
			for i in range(len(attr)-1,len(attr)-6,-1):
				#print('setUpIKFKswitch :: i = ' + str(i))
				#print('setUpIKFKswitch :: attr[i] = ' + str(attr[i]))
				conn1 = findNameFromContext(attr[i],'W0')
				#print('setUpIKFKswitch :: conn1 = ' + str(conn1))	
				if(conn1 != None):
					break

			for i in range(len(attr)-1,len(attr)-6,-1):
				conn2 = findNameFromContext(attr[i],'W1')
				#print('setUpIKFKswitch :: conn2 = ' + str(conn2))
				if(conn2 != None):
					break

			if(conn1 != None):
				if(ik == True):
					destination = c[0] + '.' + conn1
					#print('setUpIKFKswitch :: destination = ' + str(destination))
					source =  setRangeNode + '.outValueX'
					maya.cmds.connectAttr(source, destination, force=True)
					if(fk == True):
						if(conn2 != None):
							destination = c[0] + '.' + conn2
							source =  setRangeNode + '.outValueY'
							maya.cmds.connectAttr(source, destination, force=True)
							maya.cmds.setAttr(setRangeNode + '.oldMinX',10)
							maya.cmds.setAttr(setRangeNode + '.oldMinY',0)
							maya.cmds.setAttr(setRangeNode + '.oldMaxX',0)
							maya.cmds.setAttr(setRangeNode + '.oldMaxY',10)
							maya.cmds.setAttr(setRangeNode + '.minX',1)
							maya.cmds.setAttr(setRangeNode + '.minY',0)
							maya.cmds.setAttr(setRangeNode + '.maxX',0)
							maya.cmds.setAttr(setRangeNode + '.maxY',1)
					else:
						maya.cmds.setAttr(setRangeNode + '.oldMinX',10)
						maya.cmds.setAttr(setRangeNode + '.oldMinY',0)
						maya.cmds.setAttr(setRangeNode + '.oldMaxX',0)
						maya.cmds.setAttr(setRangeNode + '.oldMaxY',10)
						maya.cmds.setAttr(setRangeNode + '.minX',1)
						maya.cmds.setAttr(setRangeNode + '.minY',1)
						maya.cmds.setAttr(setRangeNode + '.maxX',1)
						maya.cmds.setAttr(setRangeNode + '.maxY',1)
			else:
				if(fk == True):
					maya.cmds.setAttr(ctrl + '.IkFk',10)
					destination = c[0] + '.' + conn1
					source =  setRangeNode + '.outValueY'
					maya.cmds.connectAttr(source, destination, force=True)
					maya.cmds.setAttr(setRangeNode + '.oldMinX',0)
					maya.cmds.setAttr(setRangeNode + '.oldMinY',0)
					maya.cmds.setAttr(setRangeNode + '.oldMaxX',10)
					maya.cmds.setAttr(setRangeNode + '.oldMaxY',10)
					maya.cmds.setAttr(setRangeNode + '.minX',1)
					maya.cmds.setAttr(setRangeNode + '.minY',1)
					maya.cmds.setAttr(setRangeNode + '.maxX',1)
					maya.cmds.setAttr(setRangeNode + '.maxY',1)

	#print('setUpIKFKswitch :: setRangeNode = ' + str(setRangeNode))
	return setRangeNode


"""
USAGE :  TODO

REQUIRES:
1. utilities.checkAttrExist

INPUTS :
1. prefix = String
2. ikArray = String Array
3. fkArray = String Array
4. ctrl = String
5. attribute = String
6. setRange = TODO

OUTPUT :
1. setRangeNode = String

NOTES : 
1. NA
""" 
def setUpIkFkVisibilitySwitch(prefix,ikArray,fkArray,ctrl,attribute,setRange):
	utilities.checkAttrExist(ctrl,attribute,'double',0,10,0,True,False)
	ikFkSwitchSetRange = prefix + 'ikFk_vis_switch_setRange'
	setRangeNode = ''

	source = ctrl + '.' + attribute

	if maya.cmds.objExists(setRange):
		setRangeNode = setRange
	else:
		if(maya.cmds.objExists(ikFkSwitchSetRange) == False):
			setRangeNode = maya.cmds.shadingNode('setRange',n=ikFkSwitchSetRange,au=True)
			maya.cmds.setAttr(setRangeNode + '.oldMinX',10)
			maya.cmds.setAttr(setRangeNode + '.oldMinY',0)
			maya.cmds.setAttr(setRangeNode + '.oldMaxX',0)
			maya.cmds.setAttr(setRangeNode + '.oldMaxY',10)
			maya.cmds.setAttr(setRangeNode + '.minX',1)
			maya.cmds.setAttr(setRangeNode + '.minY',0)
			maya.cmds.setAttr(setRangeNode + '.maxX',0)
			maya.cmds.setAttr(setRangeNode + '.maxY',1)
			
			destination = setRangeNode + '.valueX'
			maya.cmds.connectAttr(source, destination, force=True)

			destination = setRangeNode + '.valueY'
			maya.cmds.connectAttr(source, destination, force=True)
		else:
			setRangeNode = ikFkSwitchSetRange

	source = setRangeNode + '.outValueX'
	#print('setUpIkFfVisibilitySwitch :: ikArray = ' + str(ikArray))

	if(len(ikArray) > 0):
		#print('setUpIkFfVisibilitySwitch :: ik ')
		for c in ikArray:
			if maya.cmds.objExists(c):
				#print('setUpIkFfVisibilitySwitch :: ik : c = ' + str(c))
				destination = c + '.visibility'
				maya.cmds.connectAttr(source, destination, force=True)

	source = setRangeNode + '.outValueY'

	if(len(fkArray) > 0):
		#print('setUpIkFfVisibilitySwitch :: fk ')
		for c in fkArray:
			if maya.cmds.objExists(c):
				#print('setUpIkFfVisibilitySwitch :: fk : c = ' + str(c))
				destination = c + '.visibility'
				maya.cmds.connectAttr(source, destination, force=True)

	#print('setUpIkFfVisibilitySwitch :: setRangeNode = ' + str(setRangeNode))
	return setRangeNode


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. ikCtrl = String
2. ikCtrl = String 
3. splineIkCtrl = String 
4. constraintType = String
5. offset = TODO
6. name = TODO

OUTPUT :
1. constraint = String

NOTES : 
1. NA
""" 	
def setUpIKFKparent(ikCtrl, fkCtrl, splineIkCtrl, constraintType , offset, name):
	ik = None
	constraint = None
	#fk = None
	if(ikCtrl != None):
		constraint = setConstraint(constraintType, ikCtrl, splineIkCtrl, offset, name)
		if(fkCtrl != None):
			setConstraint(constraintType, fkCtrl, splineIkCtrl, offset, name)
		else:
			print('WARNING :: fkCtrl has no controls.')
	else:
		print('WARNING :: ikCtrl has no controls.')
		if(fkCtrl != None):
			constraint = setConstraint(constraintType, fkCtrl, splineIkCtrl, offset, name)
		else:
			print('WARNING :: fkCtrl has no controls.')
	return constraint


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. prefix = String
2. srceObj = String 
3. srceAttr = String 
4. destArray = String Array
5. destAttr = String

OUTPUT :
1. NA

NOTES : 
1. NA
""" 
# formerly known as ikStretchToe
def setupIkStretchToe(prefix, srceObj, srceAttr, destArray, destAttr):

	howManyJoints = len(destArray)
	brake = 0
	increment = 0
	nodes = []
	nodeName = prefix + '_multiplyDivide_'

	#CONNECT CONDITION NODE TO MULYIPLIER NODES
	for i in range(0,howManyJoints,1):
		node = maya.cmds.shadingNode('multiplyDivide',n=nodeName + str(i),au=True) 
		nodes.append(node)
		whichAxis = [ 'X', 'Y', 'Z']
		for j in range(0,3,1):
			if(brake == 0):
				#GET ATTRIBUTE OF JOINT
				value = maya.cmds.getAttr(destArray[increment] + '.' + destAttr)
				#SET ATTRIBUTE
				maya.cmds.setAttr(nodes[i] + '.' + 'input2' + whichAxis[j], value)

				#CONNECT CTRL TO MULT NODE
				source = srceObj + '.' + srceAttr
				destination = nodes[i] + '.' + 'input1' + whichAxis[j]
				maya.cmds.connectAttr(source, destination, force=True)

				source = nodes[i] + '.' + 'output' + whichAxis[j]
				destination = destArray[increment] + '.' + destAttr
				maya.cmds.connectAttr(source, destination, force=True)

				increment += 1

				#LOOP BREAK TO CATER FOR ODD NUMBER OF JOINTS
				if((increment + 1) == howManyJoints):
					brake = 1
"""
USAGE :  Connects the ........ TODO

REQUIRES:
1. NA

INPUTS :
1. rollArray = TODO
2. array = TODO
3. jointRollAxis = TODO

OUTPUT :
1. groupNodes = TODO

NOTES : 
1. NA
"""	
# Formerly known as connectRoll
def setJointRoll(rollArray,array,jointRollAxis):
	whichAxis = ['X', 'Y', 'Z']
	brk = 0
	index = 0
	groupNodes = []
	for i in range(0,len(rollArray),1):
		for j in range(0,3,1):
			if(brk == 0):
				rollGroup = maya.cmds.group(em=True, n=(array[index] + '_ROLL'))
				groupNodes.append(rollGroup)
				maya.cmds.parent(rollGroup,array[index],r=True)
				source =  rollArray[i] + '.output' + whichAxis[j]
				desitination = rollGroup + '.rotate' + jointRollAxis
				maya.cmds.connectAttr(source, desitination, force=True)
				if(index == len(array)-1):
					brk = 1
					#print('createRoll ::brk = ' + str(brk))
				index = index + 1
	
	return groupNodes


"""
USAGE :  Setups the ........ TODO

REQUIRES:
1. NA

INPUTS :
1. prefix = String
2. array = String Array
3. maxRoll = TODO
4. remapCurveValues
5. jointRollAxis = TODO
6. controlRollAxis = TODO
7. control = TODO
8. invert = TODO

OUTPUT :
1. multiplyNodes = String Array
2. groupNodes = String Array

NOTES : 
1. NA
"""	
# Formerly known as createRoll
def setupJointRoll(prefix,array,maxRoll,remapCurveValues,jointRollAxis,controlRollAxis,control,invert):
	#print('createRoll :: array = ' + str(array))
	#print('createRoll :: prefix = ' + str(prefix))
	#maxRoll = 120
	whichAxis = ['X', 'Y', 'Z']

	#cREATE TEMP REMAP SYSTEM
	inputNode = maya.cmds.shadingNode('multiplyDivide',n='rollInput_multiplyDivide' + '1',au=True)
	resultNode = maya.cmds.shadingNode('multiplyDivide',n='rollResult_multiplyDivide' + '1',au=True)
	rollRemapNode = maya.cmds.shadingNode('remapValue',n='roll_remap' + '1',au=True) 
	source =  inputNode + '.outputX'
	desitination =  rollRemapNode + '.inputValue'  

	maya.cmds.connectAttr(source, desitination, force=True)

	source =  rollRemapNode + '.outValue'
	desitination =  resultNode + '.input1X'  

	maya.cmds.connectAttr(source, desitination, force=True)
	i = 0
	for v in remapCurveValues:
		maya.cmds.setAttr(rollRemapNode + '.value[' + str(i) + '].value_Position',v[0])
		maya.cmds.setAttr(rollRemapNode + '.value[' + str(i) + '].value_FloatValue',v[1])
		maya.cmds.setAttr(rollRemapNode + '.value[' + str(i) + '].value_Interp',v[2])
		i = i + 1
	
	maya.cmds.setAttr(rollRemapNode + '.inputMin',0)
	maya.cmds.setAttr(rollRemapNode + '.inputMax',maxRoll)
	maya.cmds.setAttr(rollRemapNode + '.outputMin',0)
	maya.cmds.setAttr(rollRemapNode + '.outputMax',1)

	howManyMultiplyNodes = math.ceil(float(len(array))  / 3.0)
	#print('createRoll :: len(array)-1 = ' + str(len(array)-1))
	#print('createRoll :: maxRoll = ' + str(maxRoll))
	fraction = maxRoll / (len(array)-1)
	#print('createRoll :: fraction = ' + str(fraction))
	increment = 0#maxRoll
	index = 0
	brk = 0
	multiplyNodes = []
	groupNodes = []
	for i in range(0,howManyMultiplyNodes,1):
		rollMult = maya.cmds.shadingNode('multiplyDivide',n=prefix + 'roll_multiplyDivide' + '1',au=True)
		multiplyNodes.append(rollMult)
		for j in range(0,3,1):
			if(brk == 0):
				#print('createRoll :: increment = ' + str(increment))
				maya.cmds.setAttr(inputNode + '.input1X', increment * invert)
				result = maya.cmds.getAttr(resultNode + '.outputX')
				#print('createRoll ::result = ' + str(result))
				rollGroup = maya.cmds.group(em=True, n=(array[index] + '_ROLL'))
				#print('createRoll :: rollGroup = ' + str(rollGroup))
				groupNodes.append(rollGroup)
				maya.cmds.parent(rollGroup,array[index],r=True)
				#loc = maya.cmds.spaceLocator(n=(array[index] + '_LOC'))
				#maya.cmds.parent(loc,rollGroup,r=True)
				maya.cmds.setAttr(rollMult + '.input2' + str(whichAxis[j]), result)
				source =  control + '.rotate' + controlRollAxis
				desitination = rollMult + '.input1' + str(whichAxis[j])
				maya.cmds.connectAttr(source, desitination, force=True)
				source =  rollMult + '.output' + whichAxis[j]
				desitination = rollGroup + '.rotate' + jointRollAxis
				maya.cmds.connectAttr(source, desitination, force=True)
				increment = increment + fraction
				if(index == len(array)-1):
					brk = 1
					#print('createRoll ::brk = ' + str(brk))
				index = index + 1
		
	maya.cmds.delete(inputNode)
	maya.cmds.delete(resultNode)
	maya.cmds.delete(rollRemapNode)

	return (multiplyNodes,groupNodes)


"""
USAGE :  Setups the ........ TODO

REQUIRES:
1. NA

INPUTS :
1. prefix = String
2. array = String Array
3. maxRoll = TODO
4. remapCurveValues
5. jointRollAxis = TODO
6. controlRollAxis = TODO
7. control = TODO
8. invert = TODO

OUTPUT :
1. multiplyNodes = String Array
2. groupNodes = String Array

NOTES : 
1. NA
"""	
# Formerly known as createRoll2
def setupJointRoll02(prefix,array,maxRoll,remapCurveValues,jointRollAxis,controlRollAxis,control,invert):
	#print('createRoll :: array = ' + str(array))
	#print('createRoll :: prefix = ' + str(prefix))
	#maxRoll = 120
	whichAxis = ['X', 'Y', 'Z']

	mult = 1
	if(invert == True):
		mult = -1
	
	#CREATE TEMP REMAP SYSTEM
	inputNode = maya.cmds.shadingNode('multiplyDivide',n='rollInput_multiplyDivide' + '1',au=True)
	resultNode = maya.cmds.shadingNode('multiplyDivide',n='rollResult_multiplyDivide' + '1',au=True)
	rollRemapNode = maya.cmds.shadingNode('remapValue',n='roll_remap' + '1',au=True) 
	source =  inputNode + '.outputX'
	desitination =  rollRemapNode + '.inputValue'  

	maya.cmds.connectAttr(source, desitination, force=True)

	source =  rollRemapNode + '.outValue'
	desitination =  resultNode + '.input1X'  

	maya.cmds.connectAttr(source, desitination, force=True)
	i = 0
	for v in remapCurveValues:
		maya.cmds.setAttr(rollRemapNode + '.value[' + str(i) + '].value_Position',v[0])
		maya.cmds.setAttr(rollRemapNode + '.value[' + str(i) + '].value_FloatValue',v[1])
		maya.cmds.setAttr(rollRemapNode + '.value[' + str(i) + '].value_Interp',v[2])
		i = i + 1
	
	maya.cmds.setAttr(rollRemapNode + '.inputMin',0)
	maya.cmds.setAttr(rollRemapNode + '.inputMax',maxRoll)
	maya.cmds.setAttr(rollRemapNode + '.outputMin',0)
	maya.cmds.setAttr(rollRemapNode + '.outputMax',1)

	howManyMultiplyNodes = math.ceil(float(len(array)) / 3.0)
	#print('createRoll :: howManyMultiplyNodes = ' + str(howManyMultiplyNodes))
	#print('createRoll :: len(array)-1 = ' + str(len(array)-1))
	#print('createRoll :: maxRoll = ' + str(maxRoll))
	fraction = maxRoll / (len(array)-1)
	#print('createRoll :: fraction = ' + str(fraction))
	increment = 0 #maxRoll
	index = 0
	brk = 0
	multiplyNodes = []
	groupNodes = []
	
	for i in range(0,howManyMultiplyNodes,1):
		#print('createRoll :: i = ' + str(i))
		rollMult = maya.cmds.shadingNode('multiplyDivide',n=prefix + 'roll_multiplyDivide' + '1',au=True)
		#print('createRoll :: rollMult = ' + str(rollMult))
		multiplyNodes.append(rollMult)
		for j in range(0,3,1):
			if(brk == 0):
				#print('createRoll :: increment = ' + str(increment))
				maya.cmds.setAttr(inputNode + '.input1X', increment)
				result = maya.cmds.getAttr(resultNode + '.outputX')
				#print('createRoll ::result = ' + str(result))
				rollGroup = maya.cmds.group(em=True, n=(array[index] + '_ROLL'))
				#print('createRoll :: rollGroup = ' + str(rollGroup))
				groupNodes.append(rollGroup)
				maya.cmds.parent(rollGroup,array[index],r=True)
				maya.cmds.setAttr(rollMult + '.input2' + str(whichAxis[j]), result * mult)
				source =  control + '.rotate' + controlRollAxis
				desitination = rollMult + '.input1' + str(whichAxis[j])
				maya.cmds.connectAttr(source, desitination, force=True)
				source =  rollMult + '.output' + whichAxis[j]
				desitination = rollGroup + '.rotate' + jointRollAxis
				maya.cmds.connectAttr(source, desitination, force=True)
				increment = increment + fraction
				if(index == len(array)-1):
					brk = 1
					#print('createRoll ::brk = ' + str(brk))
				index = index + 1
	
	maya.cmds.delete(inputNode)
	maya.cmds.delete(resultNode)
	maya.cmds.delete(rollRemapNode)
	
	return (multiplyNodes,groupNodes)
	

"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. pvCtrl = TODO
2. joint = String
3. distance = Float
4. distance = Float

OUTPUT :
1. pvGrp = String

NOTES : 
1. NA
""" 
def setupPolVector(pvCtrl,joint,distance,upAxis):
	pvGrp = maya.cmds.listRelatives( pvCtrl,parent=True )[0]
	pos = getWStransform(joint)
	setWStransform(pvGrp,pos)
	rot = getWSrotate(joint)
	setWSrotate(pvGrp,rot)
	maya.cmds.parent(pvGrp,joint)
	maya.cmds.setAttr(pvGrp + '.t' + upAxis, distance)
	maya.cmds.parent(pvGrp,world=True)

	return pvGrp
	

"""
USAGE :  TODO

REQUIRES:
1. utilities.setUpGroups()

INPUTS :
1. sPrefix = TODO
2. jType = TODO
3. lTypeName = TODO
4. caa = TODO
5. jaa = TODO
6. objArray = TODO
7. crv = TODO
8. crvDiv = TODO
9. mCrtl = TODO
10. mCtrlScle = TODO
11. ignoreCurve = TODO
12. contraintType = TODO

OUTPUT :
1. NA

NOTES : 
1. NA
""" 	
def setupSplineIK02(sPrefix, jType, lTypeName, caa, jaa, objArray, crv, crvDiv, mCrtl, mCtrlScle,ignoreCurve,contraintType):
	sidePrefix = sPrefix + '_'
	jointType = jType + '_'
	limbTypeName = lTypeName + '_'
	ctrlAimAxis = caa #'X'
	jointAimAxis = jaa #'X'
	#masterSplineCTRL = mCrtl
	masterSplineCTRL = []
	#print ('buildsplineIK :: len(masterSplineCTRL) = ' + str(len(masterSplineCTRL)))
	#print ('buildsplineIK :: masterSplineCTRL = ' + str(masterSplineCTRL))
	curve = crv

	go = True

	sel = objArray 
	curveDivisions = crvDiv
	prefix = sidePrefix + jointType

	groupSkeleton = ['char_GRP','DO_NOT_ALTER_GRP','skeleton_scale_GRP','CTRL_skeleton_GRP']
	groupCurves = ['char_GRP','DO_NOT_ALTER_GRP','curves_GRP']
	groupHandles = ['char_GRP','DO_NOT_ALTER_GRP','handles_GRP',sidePrefix + jointType + limbTypeName + 'cluster_GRP']
	groupControls = ['char_GRP','DO_NOT_ALTER_GRP','controls_GRP',sidePrefix + jointType + limbTypeName + 'GRP']
	skeletonCtrlGrp = groupSkeleton[3]
	controlGrp = groupControls[3]

	#0=Right, 1=Left, 2=Centre, 3=Misc
	IKcolour = [14,13,17]
	FKColour = [23,31,25]
	splineIKColour = [6,15,29]
	clothColour = [9,30,21]
	faceColour = [22,10,26]
	misc = [4,7,11]

	if(sidePrefix == 'L_'):
		SplnCtrlColour = splineIKColour[0]
		ikctrlColour = IKcolour[0]
		fkctrlColour = FKColour[0]
	elif(sidePrefix == 'R_'):
		SplnCtrlColour = splineIKColour[1]
		ikctrlColour = IKcolour[1]
		fkctrlColour = FKColour[1]
	else:
		SplnCtrlColour = splineIKColour[2]
		ikctrlColour = IKcolour[2]
		fkctrlColour = FKColour[2]

	splineIKCtrlJoints = []
	for j in range(0,len(sel),1):
		splineIKCtrlJoints.append(sel[j])
	#print('buildsplineIK :: splineIKCtrlJoints = ' + str(splineIKCtrlJoints))

	#GET ALL JOINTS FROM SELECTED
	list = maya.cmds.listRelatives(sel[0],ad=True,typ='joint')
	reverseList = reverseArray(list)
	allJoints = []
	allJoints.append(sel[0])
	for j in range(0,len(reverseList),1):
		allJoints.append(reverseList[j])
	#print('allJoints = ' + str(allJoints))

	utilities.setUpGroups(groupCurves)
	utilities.setUpGroups(groupHandles)
	utilities.setUpGroups(groupControls)
	#print('buildsplineIK :: masterSplineCTRL = ' + str(masterSplineCTRL))

	#SETUP CONTROLS
	if(mCrtl == ''):
		#objName = sidePrefix + limbTypeName + 'SPL_Master_CTRL'
		objName = prefix + limbTypeName + 'Master_CTRL'
		if(maya.cmds.objExists(objName) != True):
			masterSplineCTRL.append(createArrowCtrl(objName,splineIKColour[2],ctrlAimAxis,mCtrlScle))
		#SET COLOUR OF NEWLY CREATED masterSplineCTRL
		setColour(masterSplineCTRL[0],SplnCtrlColour)
	else:
		masterSplineCTRL = mCrtl

	#print ('buildsplineIK :: masterSplineCTRL = ' + str(masterSplineCTRL))
	#print ('buildsplineIK :: curve = ' + str(curve))

	if(ignoreCurve == False):
		if(curve == ''):
			curve = createCurve2(splineIKCtrlJoints, prefix + limbTypeName + 'crv',curveDivisions,groupCurves[len(groupCurves)-1])[0]
		#print ('buildsplineIK :: len(masterSplineCTRL) = ' + str(len(masterSplineCTRL)))
		#print('buildsplineIK :: go = ' + str(go))
		#print('buildsplineIK :: len(masterSplineCTRL) = ' + str(len(masterSplineCTRL)))
		#TEST DEPENDANT ON WHETHER CONTROL PREBUILT ON NEED TO BE CREATED
		if(len(masterSplineCTRL) > 1):
			#maya.cmds.select(curve + '.cv[*]')
			#cvs = maya.cmds.ls(selection=True)
			cvs = getCVlist(curve)
			#print ('buildsplineIK :: cvs = ' + str(cvs))
			#print('buildsplineIK :: cvs length = ' + str(len(cvs)))
			if(len(masterSplineCTRL) != len(cvs)):
				go = False
				print('buildsplineIK :: go = ' + str(go))

	if(go == True):
		if(ignoreCurve == False):
			clusters = clusterCurve(curve,prefix + limbTypeName + 'CLUSTER_',groupHandles[len(groupHandles)-1])
			#print ('buildsplineIK :: clusters = ' + str(clusters))
			#print ('buildsplineIK :: First Joint = ' + str(splineIKCtrlJoints[0]))
			#print ('buildsplineIK :: Last Joint = ' + str(splineIKCtrlJoints[len(splineIKCtrlJoints)-1]))

			splineIK = createIKhandles2(prefix,limbTypeName,'ikSplineSolver',splineIKCtrlJoints[0],splineIKCtrlJoints[len(splineIKCtrlJoints)-1],None,curve,groupHandles[2])
	
			if(len(clusters[0]) == len(masterSplineCTRL)):
				#print ('buildsplineIK :: clusters[0] = ' + str(clusters[0]))
				#print ('buildsplineIK :: masterSplineCTRL = ' + str(masterSplineCTRL))
				#print ('buildsplineIK :: len(masterSplineCTRL) = ' + str(len(masterSplineCTRL)))
				#print ('buildsplineIK :: len(clusters[0]) = ' + str(len(clusters[0])))
				for i in range(0,len(masterSplineCTRL),1):
					#CONSTRAIN CONTROLS TO CLUSTERS
					print('buildsplineIK :: masterSplineCTRL[' + str(i) + '] = ' + str(masterSplineCTRL[i]))
					setConstraint(contraintType,masterSplineCTRL[i], clusters[0][i], True, None)

			else:
				splineIKcontrols = createSplineIKControls(splineIKCtrlJoints, masterSplineCTRL[0])
				#print('buildsplineIK :: splineIKcontrols = ' + str(splineIKcontrols))

				if(len(clusters[0]) == len(splineIKcontrols[0])):

					for i in range(0,len(splineIKcontrols[0]),1):
						aimControlsToJoints(splineIKCtrlJoints[i],splineIKcontrols[1][i],jointAimAxis)
						maya.cmds.parent(splineIKcontrols[1][i],controlGrp)
						#CONSTRAIN CONTROLS TO CLUSTERS
						setConstraint(contraintType, splineIKcontrols[0][i], clusters[0][i], True, None)
				else:
					print ('ERROR :: buildsplineIK :: Number Spline Controls does not equal number of CVs')
					for i in range(0,len(splineIKcontrols[1]),1):
						maya.cmds.delete(splineIKcontrols[1][i])

		else:
			#SPECIAL FEATURE THAT CREATES THE GROUP STRUCTURE AND CONSTRAINS THE SELCTED JOINTS TO THAT GROUP STRUCTURE
			#THERE NO SPLINE IK SOVLER USED
			splineIKcontrols = createSplineIKControls(splineIKCtrlJoints, masterSplineCTRL[0])
			#print('buildsplineIK :: splineIKcontrols = ' + str(splineIKcontrols))
			for i in range(0,len(splineIKcontrols[0]),1):
				aimControlsToJoints(splineIKCtrlJoints[i],splineIKcontrols[1][i],jointAimAxis)
				maya.cmds.parent(splineIKcontrols[1][i],controlGrp)
				#CONSTRAIN CONTROLS TO CLUSTERS
				setConstraint(contraintType, splineIKcontrols[0][i], splineIKCtrlJoints[i], True, None)

	else:
		print ('ERROR :: buildsplineIK :: Number Spline Controls does not equal number of CVs')
		

"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. jointsArray = TODO
2. masterCtrl = TODO

OUTPUT :
1. ctrlArray = String Array
2. grpArray = String Array

NOTES : 
1. NA
"""	
def setupSplineIKControls(jointsArray, masterCtrl):
	grpArray = []
	ctrlArray = []
	#create the controls
	for i in range(0, len(jointsArray), 1):
		#select only the control joints
		index = i # * divide
		#print ('index = ' + index + ';   ')
	
		copy = maya.cmds.duplicate(masterCtrl, n=(jointsArray[index] + '_CTRL'))
		#group1 = maya.cmds.group(copy[0], n=(jointsArray[index] + '_AV'))
		group2 = maya.cmds.group(copy[0], n=(jointsArray[index] + '_DYN'))
		group3 = maya.cmds.group(group2, n=(jointsArray[index] + '_GRP'))
		grpArray.append(group3)
		ctrlArray.append(copy[0])
			
		parentConstraint = maya.cmds.pointConstraint( jointsArray[index], group3)
		maya.cmds.delete(parentConstraint[0])
		
		maya.cmds.select(copy[0])
		maya.cmds.makeIdentity( apply=True, translate=True, rotate=True, scale=True, normal=False)

	return(ctrlArray,grpArray)


"""
USAGE :  TODO

REQUIRES:
1. utilities.checkAttrExist

INPUTS :
1. ctrl = TODO
2. scaleAttr = TODO
3. visAttr = TODO

OUTPUT :
1. NA

NOTES : 
1. NA
"""
def setUpSplineVisScale(ctrl,scaleAttr,visAttr):
	utilities.checkAttrExist(ctrl,visAttr,'long',0,1,1,True,False)
	utilities.checkAttrExist(ctrl,scaleAttr,'double',0,100,1,False,False)

	source1 = ctrl + '.' + scaleAttr
	source2 = ctrl + '.' + visAttr

	for c in objArray:
		if maya.cmds.objExists(c):
			print('setUpSplineVisScale :: c = ' + str(c))
			destination = c + '.sx'
			maya.cmds.connectAttr(source1, destination, force=True)
			destination = c + '.sy'
			maya.cmds.connectAttr(source1, destination, force=True)
			destination = c + '.sz'
			maya.cmds.connectAttr(source1, destination, force=True)

			destination = c + '.visibility'
			maya.cmds.connectAttr(source2, destination, force=True)


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. prefix = TODO
2. jointArray = TODO
3. ctrl = TODO

OUTPUT :
1. NA

NOTES : 
1. NA
"""	
# Formerly known as addStiffness
def setupStiffness(prefix,jointArray,ctrl):
	stiffnessAttr = 'stiffness'
	mainStiffness = ctrl + '.' + stiffnessAttr
	#print('mainStiffness = ' + str(mainStiffness))

	doesStiffnessExist = maya.cmds.attributeQuery( stiffnessAttr, node=ctrl, exists=True )
	if( doesStiffnessExist != True):
		maya.cmds.addAttr(ctrl, longName='stiffness', attributeType='double', min=0, max=10, dv=0 )
		maya.cmds.setAttr(mainStiffness,edit=True, keyable=True)

	#print('len(jointArray) = ' + str(len(jointArray)))
	if(len(jointArray) != 0):
		stretchNormaliseNode = prefix + 'stretchNormalise_setRange'
		conn = maya.cmds.listConnections( mainStiffness, d=True, s=False, t='setRange' )
		#print('conn = ' + str(conn))
		setRangeNode = ''
		if( conn == None ):
			setRangeNode = maya.cmds.shadingNode('setRange',n=stretchNormaliseNode,au=True)
			maya.cmds.setAttr(setRangeNode + '.oldMaxY', 10)
			maya.cmds.setAttr(setRangeNode + '.maxY', 1)
		elif( len(conn) == 1):
			setRangeNode = conn[0]
			#print('setRangeNode = ' + str(setRangeNode))
			maya.cmds.setAttr(setRangeNode + '.oldMaxY', 10)
			maya.cmds.setAttr(setRangeNode + '.maxY', 1)
		else:
			print('ERROR :: ' + mainStiffness + ' has too many setRange nodes connected to it!!!')

		socketAttribute1 = '.valueY'
		connectorAttribute1 = '.stiffness'

		connectorAttribute2 = '.outValueY'
		socketAttribute2 = '.stiffness'

		socket1 = setRangeNode + socketAttribute1
		connector1 = mainStiffness
		maya.cmds.connectAttr(connector1, socket1, force=True)

		for i in range(0, len(jointArray), 1):
			connector2 = setRangeNode + connectorAttribute2
	
			socket2 = jointArray[i] + (socketAttribute2 + 'X')
			maya.cmds.connectAttr(connector2, socket2, force=True)
	
			socket2 = jointArray[i] + (socketAttribute2 + 'Y')
			maya.cmds.connectAttr(connector2, socket2, force=True)

			socket2 = jointArray[i] + (socketAttribute2 + 'Z')
			maya.cmds.connectAttr(connector2, socket2, force=True)
	else:
		print('No Tween Joints to connect the Stiffness attribute')


"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. prefix = TODO
2. jointArray = TODO
3. ctrl = TODO

OUTPUT :
1. NA

NOTES : 
1. NA
"""
# Formerly known as addStiffness02
def setupStiffness02(prefix,jointArray,ctrl):
	stiffnessAttr = 'stiffness'
	mainStiffness = ctrl + '.' + stiffnessAttr
	#print('mainStiffness = ' + str(mainStiffness))

	doesStiffnessExist = maya.cmds.attributeQuery( stiffnessAttr, node=ctrl, exists=True )
	if( doesStiffnessExist != True):
		maya.cmds.addAttr(ctrl, longName='stiffness', attributeType='double', min=0, max=10, dv=0 )
		maya.cmds.setAttr(mainStiffness,edit=True, keyable=True)

	#print('len(jointArray) = ' + str(len(jointArray)))
	if(len(jointArray) != 0):
		stretchNormaliseNode = prefix + 'stiffnessNormalise_setRange'
		conn = maya.cmds.listConnections( mainStiffness, d=True, s=False, t='setRange' )
		#print('conn = ' + str(conn))
		setRangeNode = ''
		if( conn == None ):
			setRangeNode = maya.cmds.shadingNode('setRange',n=stretchNormaliseNode,au=True)
			maya.cmds.setAttr(setRangeNode + '.oldMaxY', 10)
			maya.cmds.setAttr(setRangeNode + '.maxY', 1)
		elif( len(conn) == 1):
			setRangeNode = conn[0]
			print('setRangeNode = ' + str(setRangeNode))
			maya.cmds.setAttr(setRangeNode + '.oldMaxY', 10)
			maya.cmds.setAttr(setRangeNode + '.maxY', 1)
		else:
			print('ERROR :: ' + mainStiffness + ' has too many setRange nodes connected to it!!!')

		socketAttribute1 = '.valueY'
		connectorAttribute1 = '.stiffness'

		connectorAttribute2 = '.outValueY'
		socketAttribute2 = '.stiffness'

		socket1 = setRangeNode + socketAttribute1
		connector1 = mainStiffness
		maya.cmds.connectAttr(connector1, socket1, force=True)

		for i in range(0, len(jointArray), 1):
			connector2 = setRangeNode + connectorAttribute2
	
			socket2 = jointArray[i] + (socketAttribute2 + 'X')
			maya.cmds.connectAttr(connector2, socket2, force=True)
	
			socket2 = jointArray[i] + (socketAttribute2 + 'Y')
			maya.cmds.connectAttr(connector2, socket2, force=True)

			socket2 = jointArray[i] + (socketAttribute2 + 'Z')
			maya.cmds.connectAttr(connector2, socket2, force=True)
	else:
		print('No Tween Joints to connect the Stiffness attribute')


"""
USAGE :  TODO

REQUIRES:
1. utilities.checkAttrExist

INPUTS :
1. ctrlArray = TODO
2. locatorArray = TODO
3. flexAxis = TODO

OUTPUT :
1. returnArray = String Array

NOTES : 
1. NA
"""
def setUpWingFlex(ctrlArray,locatorArray,flexAxis):
	returnArray = []
	keepVectors = []
	flexAttr = 'flex'
	utilities.checkAttrExist(ctrlArray[0],flexAttr,'double',-50,50,0,True,True)
	
	previousCtrl = ctrlArray[0]
	previousLocator = locatorArray[0]

	for j in locatorArray:
		vector = getWSrotate(j)
		print ('setUpWingFlex :: vector = ' + str(vector) )
		keepVectors.append(vector)
	
	for j in range(0,len(ctrlArray),1):
		destination = locatorArray[j] + '.rx'# + rotateAxis.lower()
		source = ctrlArray[j] + '.rx'# + rotateAxis.lower()
		maya.cmds.connectAttr(source, destination, force=True)

		destination = locatorArray[j] + '.ry'# + pitchAxis.lower()
		source = ctrlArray[j] + '.ry'# + pitchAxis.lower()
		maya.cmds.connectAttr(source, destination, force=True)

		destination = locatorArray[j] + '.rz'# + rollAxis.lower()
		source = ctrlArray[j] + '.rz'# + rollAxis.lower()
		maya.cmds.connectAttr(source, destination, force=True)
		
		constainLocator = maya.cmds.pointConstraint(locatorArray[j], ctrlArray[j], weight=1 )


	source = ctrlArray[0] + '.' + flexAttr
	for j in range(1,len(ctrlArray),1):
		maya.cmds.select(previousLocator, hi=True)
		allLoc = maya.cmds.ls(selection=True,tr=True)
		tweenLoc = filterSelection2(allLoc,locatorArray[j],1)
		
		for i in range(1,len(tweenLoc)-1,1):
			destination = tweenLoc[i] + '.r' + flexAxis.lower()
			maya.cmds.connectAttr(source, destination, force=True)
		
		previousLocator = locatorArray[j]

	grpNodes = addBaseNode(locatorArray)
	
	for j in range(0,len(grpNodes),1):
		print ('setUpWingFlex :: keepVectors[j] = ' + str(keepVectors[j]) )
		setWSrotate(grpNodes[j],keepVectors[j])
			
	return returnArray

print("Line 2144 :: Imported the utilitiesRigging Module!!!")	