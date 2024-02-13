import maya.cmds
import random
import math

ver = ' : ver 01.002 ' # This needs to be updated each time the script is updated or modified.
print ("#### Imported Utilities UI Module " + ver)


def getVersion():
	print ("Imported Utilities UI Module " + ver)
	
#def isOk():
#	print("yes")

"""
USAGE : Deletes Instance of Maya GUI Window.

REQUIRES:
1. maya.cmds.*

INPUTS :
1. windowName = String 

OUTPUTS :
1. NA

NOTES : 
1. NA
"""
def deleteWindow( windowName ):
	exist = maya.cmds.window( windowName, exists=True )
	if(exist == 1):
		maya.cmds.deleteUI(windowName, window=True)


"""
USAGE : TODO

REQUIRES:
1. maya.cmds.*

INPUTS :
1. array = String Array
2. name = String
3. type = String

OUTPUTS :
1. NA

NOTES : 
1. NOTE : This function did not have an array argument
"""
def editTxtGrpButtonSelection(name,type):
	arr = maya.cmds.ls(selection=True)
	out = ''
	for i in arr:
		out = out + i + '    '
		
	if(type == 'textFieldButtonGrp'):
		maya.cmds.textFieldButtonGrp( name, e=True, text=out)
		

"""
USAGE : TODO

REQUIRES:
1. NA

INPUTS :
1. item = String 
2. name = String  
3. type = String

OUTPUTS :
1. NA

NOTES : 
1. NOTE : This function did not have an item argument
"""		
def editTxtGrpButton(item,name,type):
	#item = maya.cmds.ls(selection=True)
	#if(len(item) == 1):
	if(type == 'textFieldButtonGrp'):
		maya.cmds.textFieldButtonGrp( name, e=True, text=str(item))
	#else:
	#	print('ERROR :: Select one item only, current items selected : ' + str(item))
		

"""
USAGE : TODO

REQUIRES:
1. The user to select a 

INPUTS :
1. array = String Array
2. name = String
3. type = String

OUTPUTS :
1. NA

NOTES : 
1. NOTE : This function did not have an array argument
"""				
#def editTxtGrpButtonArray(name,type):
def editTxtGrpButtonArray(arr, name,type):
	#arr = maya.cmds.ls(selection=True)
	out = ''
	for i in arr:
		out = out + i + '    '
		
	if(type == 'textFieldButtonGrp'):
		maya.cmds.textFieldButtonGrp( name, e=True, text=out)


"""
USAGE : TODO

REQUIRES:
1. NA

INPUTS :
1. arr = String Array
2. checkAttr = Boolean
3. fieldName = String
4. fieldType = String

OUTPUTS :
1. NA

NOTES : 
1. NOTE : TODO
"""	
def updateTextFieldButtonGrp(arr,checkAttr,fieldName,fieldType):		
	errorTxt = ''
	hasCorrectAttribute = True
	
	# Test to make sure the correct type of objects are selected.
	if not arr:
		errorTxt = 'ERROR : Nothing is selected. Select objects to connect to.'
		print(errorTxt)
		editTxtGrpButton(errorTxt,fieldName,fieldType)
	else:
		for a in arr:
			attrExist = maya.cmds.attributeQuery(checkAttr, node=a, exists=True) # example maya.cmds.attributeQuery('tx', node='pCube1', exists=True)
			# Test if selection has the correct attribute to be connected to has the correct attribute
			if hasCorrectAttribute:
				if not attrExist:
					errorTxt = 'ERROR : Selected object '+ str(a) + ' does not have the following attribute ' + str(checkAttr) + '. All selected objects must has attribute ' + str(checkAttr)
					print( errorTxt )
					hasCorrectAttribute = False
			
		if hasCorrectAttribute:
			editTxtGrpButtonArray(arr,fieldName,fieldType)
		else:
			editTxtGrpButton(errorTxt,fieldName,fieldType)		

"""
USAGE : TODO

REQUIRES:
1. NA

INPUTS :
1. windowName = String

OUTPUTS :
1. NA

NOTES : 
1. NA
"""			
def togglesystems(windowName):
	getCrv = maya.cmds.textFieldButtonGrp( windowName + '_curve', q=True, text=True )
	crve = getCrv.split()
	if(len(crve) > 0):
		maya.cmds.intFieldGrp( windowName + '_curveDivisions', e=False )
	else:
		maya.cmds.intFieldGrp( windowName + '_curveDivisions', e=True )