import maya.cmds
#import random
import math


ver = ' : ver 01.005 ' # This needs to be updated each time the script is updated or modified.
comment = 'Added setUpGroups function'
print ("#### Imported Utilities Module " + ver)

def getVersion():
	print ("Imported Utilities Module " + ver)

"""
USAGE : Loops through a list of Nodes add selected Attribute to Selected Object and connect it to a Source Object.

REQUIRES:
1. maya.cmds.*

INPUTS :
1. cntrl = String (Name of source object)
2. objArray = Array String (list of destination objects)
3. suffix = Array String (list of Strings)
4. type = String (specifies attribute type)
5. min = Array String (list of Strings)
6. max = Float (maximum value of the attribute)
7. default= Float (sets the value of the attribute)
8. keyable = Boolean
9. attr = String

OUTPUTS :
1. NA

NOTES : 
1. NA
"""
def addAttrConnect(cntrl,objArray,suffix,type,min,max,default,keyable,attr):

	for o in objArray:
		checkAttrExist(cntrl,o + suffix,type,min,max,default,keyable,True)
		destination = o + '.' + attr
		source =  cntrl + '.' + o + suffix
		maya.cmds.connectAttr(source, destination, force=True)


"""
USAGE : Loops through a list of Nodes to create a group node for each node listed in the Array object.

REQUIRES:
1. maya.cmds.*

INPUTS :
1. array = Array String (list of Strings)
2. suffix = String

OUTPUTS :
1. returnArray = Array (list of Strings)

NOTES : 
1. array is a list of node that may be based on a selection using the maya list command.
2. suffix is a String value appended to the end of the duplicated object : loc e.g suffix = "_GRP".
"""
def addBaseNode(array,suffix):
	returnArray = []
	for i in array:
		# Duplicate node and add
		loc = maya.cmds.duplicate(i,n=i + suffix)[0]
		returnArray.append(loc)
		rel = maya.cmds.listRelatives(loc,c=True,f=True)
		# Remove shape nodes to leave transform
		for r in rel:
			if maya.cmds.objExists(r):
				maya.cmds.delete(r)
		maya.cmds.parent(i,loc,a=True)
	return returnArray	
	
	
"""
USAGE : Test whether a particular attribute exists on a maya node and that its attributes have the correct parameters.

REQUIRES:
1. maya.cmds.*

INPUTS :
1. obj = String (name of Maya node that contains the attribute to check if it exists)
2. attr= String (name of attribute)
3. type = String (specifies attribute type)
4. min = Float (minimum value of the attribute)
5. max = Float (maximum value of the attribute)
6. default= Float (sets the value of the attribute)
7. keyable = Boolean 
8. replace = Boolean (if the attribute exists, replace if True, in False, do not replace the attribute)

OUTPUTS :
array object :
1. attrExist = Boolean
2. newAttr = String (name of new attributed created)

NOTES : 
1. If the attribute being checked does not exists, it is created.
2. If it does exist and has the replace option marked as True, then the attribute is deleted and replaced.
3. If it does exist and has the replace option marked as False, then the attribute is unchanged.
"""
def checkAttrExist(obj,attr,type,min,max,default,keyable,replace):
	attrExist = maya.cmds.attributeQuery(attr, node=obj, exists=True)
	newAttr = ''
	if(attrExist == False):
		newAttr = maya.cmds.addAttr(obj, longName=attr, at=type, defaultValue=default, minValue=min, maxValue=max )
		if(keyable == True):
			maya.cmds.setAttr(obj + '.' + attr, e=True, keyable=True)
		else:
			maya.cmds.setAttr(obj + '.' + attr, e=True, keyable=False, channelBox=True)
	else:
		if(replace == True):
			maya.cmds.deleteAttr(obj, at=attr)
			newAttr = maya.cmds.addAttr(obj, longName=attr, at=type, defaultValue=default, minValue=min, maxValue=max )
			if(keyable == True):
				maya.cmds.setAttr(obj + '.' + attr, e=True, keyable=True)
			else:
				maya.cmds.setAttr(obj + '.' + attr, e=True, keyable=False, channelBox=True)
	return (attrExist,newAttr)
	

"""
USAGE : Connect a given Channel Attribute of a Maya node to the given Channel Attribute to multiple Maya nodes.

REQUIRES:
1. NA

INPUTS :
1. array = String Array (list of Strings)
2. object = String 
3. srcAxis = String Array ; Example ["x","X"]
4. destAxis = String  ; Example ["x","X"]
5. srcAttr = String
6. destAttr = String

OUTPUT :
1. NA

NOTES : 
1. EXAMPLE; Connecting the Scale X attribute of a control curve to the Translate X of Multiple control curves.
"""
# From connectScale(array,object)
def connectAttrMulti(srcObj,destArray,srcAxis,destAxis,srcAttr,destAttr):
	howManyMultiplyNodes = 1
	howManyObjects = len(destArray)
	brk = 0
	
	sa = srcAttr + srcAxis[0] # example 'rz'
	da = destAttr + destAxis[0] # example 'sy'

	if(howManyObjects>3):
		howManyMultiplyNodes = int(math.ceil(float(howManyObjects) / float(3))) # Else, it is assumed only 1 Multiply node is required

	increment = 0
	whichAxis = ['X','Y','Z']

	for i in range(0, howManyMultiplyNodes, 1):
		source = srcObj + '.' + sa # example 'sx'
		
		mn = maya.cmds.shadingNode('multiplyDivide', n='scaler' + str(i), au=True)
		#print(howManyObjects)
		destination = mn + '.' + 'input1X'
		maya.cmds.connectAttr(source, destination, force=True)
		destination = mn + '.' + 'input1Y'
		maya.cmds.connectAttr(source, destination, force=True)
		destination = mn + '.' + 'input1Z'
		maya.cmds.connectAttr(source, destination, force=True)
		
		
		for j in range(0, 3, 1):
			if(brk==0):
				#print( "utilities.connectAttrMulti.brk = " + str(brk) )
				t = maya.cmds.getAttr( destArray[increment] + '.' + da ) # example da = 'tx'
				#print(howManyObjects)
				maya.cmds.setAttr(mn + '.' + 'input2' + whichAxis[j],t)
				source = mn + '.' + 'output' + whichAxis[j]
				destination = destArray[increment] + '.' + da # example da = 'tx' 
				maya.cmds.connectAttr(source, destination, force=True)
			
				increment += 1
				#print( "utilities.connectAttrMulti.len(destArray) = " + str(len(destArray)) )
				#print( "utilities.connectAttrMulti.increment = " + str(increment) )
				if(increment >= len(destArray)):
					brk = 1
					#print( "utilities.connectAttrMulti.brk = " + str(brk) )
		

"""
USAGE : TODO

REQUIRES:
1. NA

INPUTS :
1. type = String 
2. name = String 
3. howMany = Integer

OUTPUT :
1. groupNodes = String Array

NOTES : 
1. NA
"""
def createShadeNode(type, name, howMany):
	nodes = []
	for i in range(0,howMany,1):
		nodes = maya.cmds.shadingNode('multiplyDivide',n='rollInput_multiplyDivide' + '1',au=True)
	return groupNodes					
					

"""
USAGE : TODO

REQUIRES:
1. setWStransform
2. setWSrotate

INPUTS :
1. obj = String 
2. name = String 

OUTPUT :
1. newGrp = String

NOTES : 
1. NA
"""
# Formerly known as createEmptyGroupBaseOnObj
def createEmptyGroupFromObj(obj, name):
	newGrp = maya.cmds.group(em=True,n=name + '_GRP')
	#print('checkAttrExist :: newGrp = ' + str(newGrp))
	position = getWStransform(obj)
	rotate = getWSrotate(obj)
	setWStransform(newGrp,position)
	setWSrotate(newGrp,rotate)
	
	return newGrp
		

		
		

"""
USAGE : TODO

REQUIRES:
1. createEmptyGroupFromObj

INPUTS :
1. objArray = String Array
2. grpNameArray = String Array

OUTPUT :
1. NA

NOTES : 
1. NA
"""
# Formerly known as createMultiEmptyGroupBaseOnObj
def createEmptyGroupFromObjMulti(objArray, grpNameArray):
	masterObj = objArray[0]
	lastChar = masterObj.rfind('_')
	masterGrp = createEmptyGroupFromObj(masterObj,masterObj[0:lastChar])
	for obj in objArray:
		previousGrp = ''
		for i in range(0,len(grpNameArray),1):
			grp = createEmptyGroupFromObj(obj,obj + '_' + grpNameArray[i])
			if maya.cmds.objExists(previousGrp):
				maya.cmds.parent(grp,previousGrp)
			else:
				maya.cmds.parent(grp,masterGrp)
				maya.cmds.parentConstraint(obj,grp)
			previousGrp = grp
	
	
"""
USAGE : Loops through a String Array and test whether the selected String ends with suffix String.

REQUIRES:
1. NA

INPUTS :
1. array = String Array (list of Strings)
2. suffix = String 

OUTPUT :
1. value = String

NOTES : 
1. NA
"""
# Formerly known as findNameFromContextArray
def findNameFromSuffixArray(array,suffix):
	value = None
	for a in array:
		test = a.endswith(suffix)
		if(test == True):
			value = a
	return value

	
"""
USAGE : Tests whether the Input String ends with suffix String. 

REQUIRES:
1. NA

INPUTS :
1. name = String 
2. suffix = String 

OUTPUT :
1. value = String

NOTES : 
1. NA
"""
# Formerly known as findNameFromContext
def findNameFromSuffix(name,suffix):
	value = None
	test = name.endswith(suffix)
	if(test == True):
		value = name
	return value


"""
USAGE :  Returns a limited list of nodes based on a breakerObj. Use it return only the joints of a leg rig prior to the foot joints for instance.

REQUIRES:
1. NA

INPUTS :
1. array = Array String
2. breakerObj = String
3. increment = Integer

OUTPUT :
1. NA

NOTES : 
1. breakerObj = a node that is included in the array parameter. It is use to limit the nodes to be returned
2. increment = generally set to 1, but can be set to 2 to return every second joint for instance
""" 
def filterSelection(array,breakerObj,increment):
	newArray = []
	for n in range(0,len(array),increment):
		if(brake == False):
			newArray.append(array[n])
			if(array[n] == breakerObj):
				break
	return newArray


"""
USAGE : Tests whether the Input String contains String token. 

REQUIRES:
1. NA

INPUTS :
1. name = String 
2. token = String 

OUTPUT :
1. newName = String

NOTES : 
1. NA
""" 
def findName(name,token):
	newName = name[len(token):len(name)]	
	return newName
	

"""
USAGE : TODO 

REQUIRES:
1. NA

INPUTS :
1. find = String 
2. replace = String 

OUTPUT :
1. NA

NOTES : 
1. NA
""" 	
def findReplace(find,replace):
	collect = []
	sp = maya.cmds.textFieldGrp( windowName + '_sidePrefix', q=True, text=True )
	sps = sp.split()
	for i in range(0,len(sps),1):
		collect.append(sps[i])
	jt = maya.cmds.textFieldGrp( windowName + '_jointType', q=True, text=True )
	jts = jt.split()
	for i in range(0,len(jts),1):
		collect.append(jts[i])
	lt = maya.cmds.textFieldGrp( windowName + '_limbTypeName', q=True, text=True )
	lts = lt.split()
	for i in range(0,len(lts),1):
		collect.append(lts[i])
	jaa = maya.cmds.radioButtonGrp( windowName + '_jointAimAxis', q=True, sl=True )
	jointAimAxis = whichAxis(jaa)[1]
	getMainCtrl = maya.cmds.textFieldButtonGrp( windowName + '_mainCtrl', q=True, text=True )
	mainCtrl = getMainCtrl.split()[0]
	getStartCtrl = maya.cmds.textFieldButtonGrp( windowName + '_startCtrl', q=True, text=True )
	startCtrl = getStartCtrl.split()[0]
	getEndCtrl = maya.cmds.textFieldButtonGrp( windowName + '_endCtrl', q=True, text=True )
	endCtrl = getEndCtrl.split()[0]
	getJoints = maya.cmds.textFieldButtonGrp( windowName + '_joints', q=True, text=True )
	joints = getJoints.split()
	getIkHandle = maya.cmds.textFieldButtonGrp( windowName + '_ikHandle', q=True, text=True )
	mainIkhandle = getIkHandle.split()
	getGroup = maya.cmds.textFieldButtonGrp( windowName + '_grp', q=True, text=True )
	groupDim = getGroup.split()


"""
USAGE :  Get the distance between two points.

REQUIRES:
1. NA

INPUTS :
1. pointA = Vector
2. pointB = Vector

OUTPUT :
1. distance

NOTES : 
1. NA
""" 
def getDistance2Vectors(pointA,pointB):
	sp = getWStransform(pointA)
	ep = getWStransform(pointB)
	distance = math.sqrt(  math.pow(sp[0]-ep[0],2) + math.pow(sp[1]-ep[1],2) + math.pow(sp[2]-ep[2],2)  )
	return distance


"""
USAGE : Gets the String name of the Shape Node that is connected to the Maya Transforms node listed in the functions argument.

REQUIRES:
1. NA

INPUTS :
1. obj = String

OUTPUT :
1. getShape = String
2. howManyShapes = Integer

NOTES : 
1. NA
""" 
def getShapeNodes(obj):
	howManyShapes = 0
	getShape = maya.cmds.listRelatives(obj, shapes=True)
	if(getShape == None):
		print 'ERROR:: getShapeNodes : No Shape Nodes Connected to ' + obj + ' /n'
	else:
		howManyShapes = len(getShape[0])
	return (getShape, howManyShapes)


"""
USAGE :  Get World Space Rotation angle.

REQUIRES:
1. NA

INPUTS :
1. obj = String

OUTPUT :
1. rotate

NOTES : 
1. NA
""" 
def getWSrotate(obj):
	rotate = maya.cmds.xform( obj, q=True, ws=True, ro=True )
	return rotate


"""
USAGE :  Get World Space Transform.

REQUIRES:
1. NA

INPUTS :
1. obj = String

OUTPUT :
1. transform

NOTES : 
1. NA
""" 
def getWStransform(obj):
	transform = maya.cmds.xform( obj, q=True, ws=True, t=True )
	return transform



"""
USAGE :  TODO

REQUIRES:
1. NA

INPUTS :
1. aimAxis = Vecor

OUTPUT :
1. transform

NOTES : 
1. NA
""" 	
def getPitchAxis(aimAxis,upAxis):
	pitchAxis = 'x'
	if(aimAxis == 'x' and upAxis == 'z'):
		pitchAxis = 'y'
	elif(aimAxis == 'x' and upAxis == 'y'): 
		pitchAxis = 'z'
	
	return pitchAxis


def getVector(axis):
	#axis = axis.lower()
	returnVector = [1,0,0]
	if(axis == 'y'):
		returnVector[0] = 0
		returnVector[1] = 1
		returnVector[2] = 0
	elif(axis == 'z'):
		returnVector[0] = 0
		returnVector[1] = 0
		returnVector[2] = 1

	return returnVector

"""
USAGE :  Loops through Array and groups the selected Maya object.

REQUIRES:
1. NA

INPUTS :
1. objArray = Array String
2. replaceText = String
3. grpNameArray = Array String

OUTPUT :
1. NA

NOTES : 
1. NA
""" 
def grpSelObj(objArray,replaceText,grpNameArray):
	masterObj = objArray[0]
	lastChar = masterObj.rfind('_')
	newText = ''
	if(len(grpNameArray) > 1):
		newText = '_' + grpNameArray[0]
	
	for obj in objArray:
		if(len(replaceText) > 1):
			newObjName = replaceText[0]
		else:
			newObjName = obj
		grp = createEmptyGroupBaseOnObj(obj,newObjName + newText)
		maya.cmds.parent(obj,grp)
		

"""
USAGE :  Outputs vector of selected axis.

REQUIRES:
1. NA

INPUTS :
1. increment = Integer
2. value = Integer
3. axis = String

OUTPUT :
1. vector

NOTES : 
1. NA
""" 
def incrementPos(increment,value,axis):
	vector = (0,0,0)
	value = value + increment
	if(axis == 'x'):
		vector = (value,0,0)
	elif(axis == 'y'):
		vector = (0,value,0)
	else:
		vector = (0,0,value)
	return vector


"""
USAGE : Set attributes of selected object, locks and hides it attributes.

REQUIRES:
1. NA

INPUTS :
1. obj = String
2. attrArray = String Array (list of Strings)
3. lock = Boolean
4. hide = Boolean

OUTPUT :
1. returnArray = String Array of the altered String

NOTES : 
1. NA
""" 
def lockHideAttr(obj,attrArray,lock,hide):
	for a in attrArray:
		maya.cmds.setAttr(obj + '.' + a, k=hide,l=lock)


"""
USAGE : TODO

REQUIRES:
1. getWStransform
2. getWSrotate

INPUTS :
1. obj = String
2. sourceObj = String

OUTPUT :
1. NA

NOTES : 
1. NA
""" 
def matchPosRot(obj,sourceObj):
	pos = getWStransform(sourceObj)
	rot = getWSrotate(sourceObj)
	setWStransform(obj,pos)
	setWSrotate(obj,rot)

	
"""
USAGE : Renames the obj String name by removing the suffix from the String. 

REQUIRES:
1. NA

INPUTS :
1. obj = String 
2. sourceObj = String 
2. suffix = String 

OUTPUT :
1. newObj = altered String

NOTES : 
1. NA
""" 
def matchRemoveSuffix(obj,sourceObj,suffix):
	oldName = sourceObj
	replaceSuffix = oldName.rfind(suffix)
	newName = oldName[0:replaceSuffix]
	newObj = maya.cmds.rename(obj,newName)
	return newObj

	
"""
USAGE : Appends prefix and suffix String to the each String listed in the array object. 

REQUIRES:
1. NA

INPUTS :
1. array = String Array (list of Strings)
2. prefix = String 
2. suffix = String 

OUTPUT :
1. returnArray = String Array of the altered String

NOTES : 
1. NA
""" 
def renamePrefixSuffix(array,prefix,suffix):
	returnArray = []
	for item in array:
		temp = maya.cmds.rename(item,prefix + item + suffix)
		returnArray.append(temp)
	return returnArray



"""
USAGE : Reverses the order of the list of String array.

REQUIRES:
1. NA

INPUTS :
1. array = String Array (list of Strings)
2. sourceObj = String 
3. suffix = String 

OUTPUT :
1. returnArray = String Array of the altered String

NOTES : 
1. NA
""" 
def reverseArray(array):
	retrunArray = []
	for i in range(len(array)-1,-1,-1):
		retrunArray.append(array[i])
	return retrunArray


"""
USAGE : Sets the override colour of a Maya node.

REQUIRES:
1. getShapeNodes

INPUTS :
1. array = String Array (list of Strings)
2. colour = Integer

OUTPUT :
1. NA

NOTES : 
1. NA
""" 
def setColour(array,colour):
	print("setColour from utilities module")
	for a in array:
		if maya.cmds.objExists(a):
			shape = getShapeNodes(a)
			maya.cmds.setAttr(shape[0][0] + '.overrideEnabled',1)
			maya.cmds.setAttr(shape[0][0] + '.overrideColor', colour)


"""
USAGE : TODO

REQUIRES:
1. NA
2. NA

INPUTS :
1. obj = String 
2. name = String 

OUTPUT :
1. newGrp = String

NOTES : 
1. NA
"""
# Formerly known as setUpGrp
def setUpGroups(array):
	i = 0
	previous = array[0]
	for a in array:
		exist = maya.cmds.objExists(a)
		if(exist == False ):
			maya.cmds.group(em=True,n=a,w=True)
			if(i > 0 ):
				maya.cmds.parent(a,previous,r=True)
		i = i + 1
		previous = a


		
"""
USAGE : Sets the override colour of a Maya node.

REQUIRES:
1. NA

INPUTS :
1. obj = String
2. position = Vector

OUTPUT :
1. NA

NOTES : 
1. NA
""" 			
def setWStransform(obj,position):
	maya.cmds.xform( obj, ws=True, t=(position[0],position[1],position[2]) )


"""
USAGE : Sets the override colour of a Maya node.

REQUIRES:
1. NA

INPUTS :
1. obj = String
2. rotate = Vector

OUTPUT :
1. NA

NOTES : 
1. NA
""" 
def setWSrotate(obj,rotate):
	maya.cmds.xform( obj, ws=True, ro=(rotate[0],rotate[1],rotate[2]) )		
			
		
"""
USAGE : Outputs which axis. Outputs an array of 2 characters (lower case and upper case) representing an 3D axis. Input is an integer 1,2 or 3

REQUIRES:
1. NA

INPUTS :
1. value = Integer

OUTPUT :
1. axis = String Array

NOTES : 
1. NA
""" 
def whichAxis(value):
	axis = ['x','X']
	if(value == 2):
		axis = ['y','Y']
	elif(value == 3):
		axis = ['z','Z']
	return axis		
		

"""
USAGE : Outputs a string reflecting the name of a Maya constraint type. Input is an integer 1,2 or 3 .

REQUIRES:
1. NA

INPUTS :
1. value = Integer

OUTPUT :
1. distance

NOTES : 
1. NA
""" 
def whichConstaintType(value):
	axis = 'parent'
	if(value == 2):
		axis = 'point'
	elif(value == 3):
		axis = 'aim'
	return axis
	
	
print("Line 780 :: Imported the utilities Module!!!")	