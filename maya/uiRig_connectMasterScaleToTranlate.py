import sys


# Import Python and Maya modules
import maya.cmds
import random
import math


# Import custom modules
import utilities as utl # Generic utility functions that is meant to be used for multiply tasks in Maya.
import utilitiesCurves as uCrv # Maya Curve related utility functions.
import utilitiesRigging as uRig # Maya Rigging related utility functions.
import utilitiesUI as ui # Maya UI Element related utility functions.


###############################################################################################
#   INSTRUCTIONS FOR USE.
#	TODO:	
#	1. TODO
#	
#	
###############################################################################################

# Define local UI Variables
line00 = '	SPECIFIY THE CONTROL AIM AXIS:-'
line01 = '	SELECT MASTER CONTROL :-'  #TYPE PREFIX :-'
line02 = '	SELECT OBJECT TO CONNECT TO :-'


ver = ' : ver 01.005 ' # This needs to be updated each time the script is updated or modified.
windowTitle = 'Connects Master Scale Attribute to Translate'
rebuildWindowName = 'connectMasterScleToTrans'


# Define Global Variables
gSrcAttr = 'scale'
gDestAttr = 'translate'

gCtrlAimAxis = '_ctrlAimAxis'
gMasterCtrl = '_masterCtrl'
gDestCtrl = '_destCtrl'


# Define Local Functions
"""
USAGE : TODO

REQUIRES:
1. NA

INPUTS :
1. wndwName = String 
2. fieldType = String 

OUTPUTS :
1. NA

NOTES : 
1. NOTE : TODO
"""		
def ui_getSetSelectSource(wndwName,fieldType):
	# Get the selected objects.
	arr = []
	sel = maya.cmds.ls(selection=True)
	if sel:
		arr.append(sel[0])
	#print arr
	
	fieldAxis = wndwName + gCtrlAimAxis #'_ctrlAimAxis'
	fieldName = wndwName + gMasterCtrl #'_masterCtrl'
	
	# Get the axis to check the if the objects have the correct attribute
	caa = maya.cmds.radioButtonGrp( fieldAxis, q=True, sl=True )
	ctrlAimAxis = utl.whichAxis(caa)
	
	# To check to make sure the attribute exists
	checkAttr = gDestAttr + ctrlAimAxis[1] # example 'tx' or 'ry'
	
	ui.updateTextFieldButtonGrp(arr,checkAttr,fieldName,fieldType)
	
	
"""
USAGE : TODO

REQUIRES:
1. NA

INPUTS :
1. wndwName = String 
2. fieldType = String  

OUTPUTS :
1. NA

NOTES : 
1. NOTE : TODO
"""		
def ui_getSetSelectDestination(wndwName,fieldType):
	# Get the selected objects.
	arr = maya.cmds.ls(selection=True)
	
	fieldAxis = wndwName + gCtrlAimAxis #'_ctrlAimAxis'
	fieldName = wndwName + gDestCtrl #'_destCtrl'
	
	# Get the axis to check the if the objects have the correct attribute
	caa = maya.cmds.radioButtonGrp( fieldAxis, q=True, sl=True )
	ctrlAimAxis = utl.whichAxis(caa)
	
	# To check to make sure the attribute exists
	checkAttr = gDestAttr + ctrlAimAxis[1] # example 'tx' or 'ry'
	
	ui.updateTextFieldButtonGrp(arr,checkAttr,fieldName,fieldType)


def buildWindow(inj, windowName, windowTitle, line00, line01, line02):
	
	#arr = ['1','2','3'] # Temp for testing, needs to be removed
	questionButtonHeight=23
	maya.cmds.window( windowName, title= windowTitle, s=True, iconName='Short Name', widthHeight=(500, 600))
	maya.cmds.frameLayout(  windowName + '_frameLayout1', label=' ', borderStyle="in", lv=False, bv=False, mw=10, mh=10)
	maya.cmds.columnLayout(windowName + '_column1', adjustableColumn=True)

	maya.cmds.text( label= '   ' )

	maya.cmds.rowLayout(windowName + '_row1',numberOfColumns=3, columnWidth3=(80, 80, 80), adjustableColumn3=3, columnAlign3=('left','left','left'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
	
	maya.cmds.text( label= '   ' )
	maya.cmds.text( label= '   ' )
	maya.cmds.text( label= '   ' )
	maya.cmds.setParent('..')

	maya.cmds.text( label= '   ' )

	maya.cmds.frameLayout(windowName + '_formBase', label='Tabs', lv=False, labelAlign='top', borderStyle='in')
	maya.cmds.rowLayout(windowName + '_row2',numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn2=2, columnAlign2=('left','left'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
	
	maya.cmds.columnLayout(windowName + '_global1a', rs=3)
	maya.cmds.text( label= line00 )
	maya.cmds.radioButtonGrp( windowName + gCtrlAimAxis, label='Control Aim Axis:', labelArray3=['x', 'y', 'z'], numberOfRadioButtons=3, en=True, sl=1 )
	maya.cmds.text( label= line01 )
	#cmd1 = inj + '.ui_getSetSelectSource("' + windowName + '","textFieldButtonGrp")'
	cmd1 = 'ui_getSetSelectSource("' + windowName + '","textFieldButtonGrp")'
	maya.cmds.textFieldButtonGrp( windowName + gMasterCtrl, label='Get Master Control:', text='', buttonLabel='Select', cc='togglesystems("' + windowName + '")', bc=cmd1, en=True )
	maya.cmds.text( label= line02 )
	#cmd2 = inj + '.ui_getSetSelectDestination("' + windowName + '_destCtrl' + '","textFieldButtonGrp")'
	cmd2 = 'ui_getSetSelectDestination("' + windowName + '","textFieldButtonGrp")'
	maya.cmds.textFieldButtonGrp( windowName + gDestCtrl, label='Destination Controls:', text='', buttonLabel='Select', cc='togglesystems("' + windowName + '")', bc=cmd2, en=True )
	maya.cmds.setParent('..')

	maya.cmds.columnLayout(windowName + '_global1b', rs=3)
	maya.cmds.text( label= '   ' )
	maya.cmds.button(label='?', height = questionButtonHeight)
	maya.cmds.text( label= '   ' )
	maya.cmds.button(label='?', height = questionButtonHeight)
	maya.cmds.text( label= '   ' )
	maya.cmds.setParent('..')
	
	maya.cmds.setParent('..')

	maya.cmds.text( windowName + '_space1', label='' )
	maya.cmds.text( windowName + '_space2', label='' )
	
	cmd3 = inj + '.runWindow("' + windowName + '")'
	maya.cmds.button(windowName + '_CreateSystem', label='Run Script', c=cmd3 )

	maya.cmds.showWindow( windowName )


def runWindow(windowName):
	caa = maya.cmds.radioButtonGrp( windowName + gCtrlAimAxis, q=True, sl=True )	
	ctrlAimAxis = utl.whichAxis(caa)
	#print( "ctrlAimAxis = " + str(ctrlAimAxis) )
	
	getCtrl = maya.cmds.textFieldButtonGrp( windowName + gMasterCtrl, q=True, text=True )
	ctrlArray = getCtrl.split()
	srcCntrl = ctrlArray[0]
	#print( "srcCntrl = " + str(srcCntrl) )
	
	getDestCtrl = maya.cmds.textFieldButtonGrp( windowName + gDestCtrl, q=True, text=True )
	destCtrlArray = getDestCtrl.split()
	
	# connectAttrMulti(srcObj,destArray,srcAxis,destAxis,srcAttr,destAttr)
	utl.connectAttrMulti(srcCntrl,destCtrlArray,ctrlAimAxis,ctrlAimAxis,'s','t')
	#print "Run Window"




# Run the functions	
def run(inject):
	# Clears the old instance of the window is it exists.
	ui.deleteWindow(rebuildWindowName) 

	# 
	buildWindow(inject,rebuildWindowName,windowTitle,line00,line01,line02)

print("line 0197 :: Imported uiRig_connectMasterScaleToTranlate Module")