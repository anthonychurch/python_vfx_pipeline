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

#print(ui)

###############################################################################################
#   INSTRUCTIONS FOR USE.
#	TODO:	
#	1. TODO
#	2. TODO
#	3. TODO
###############################################################################################


# Define local UI Variables
line1 = '	TYPE IN THE SIDE PREFIX ie: L or R:-'
line2 = '	TYPE IN THE NAME OF THE JOINT ie: IK or SPL:-'
line3 = '	SELECT THE JOINTS TO BE COPIED:-'
line4 = '	EITHER REPLACE EXISTING DEFAULT GROUP NAMES THAT ARE IN THE TEXT FIELD BY RENAMING THEM OR SELECTING AND ADDING EXISTING GROUP NODES:-'

ver = ' : ver 01.002 ' # This needs to be updated each time the script is updated or modified.
windowTitle = 'Copy selected Joints' + ver
rebuildWindowName = 'CopySelectedJoints'

# Define local functions


def buildWindow(thisModule,uiModule,windowName,windowTitle, line01, line02, line03, line04):
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
	
	maya.cmds.text( label= line01 )
	cmdBc01 = uiModule + '.' + 'editTxtGrpButtonSelection("' + windowName + '_sidePrefix' + '","textFieldButtonGrp")'
	maya.cmds.textFieldButtonGrp( windowName + '_sidePrefix', label='Get Side Prefix:', text='L', buttonLabel='Select', en=True, bc=cmdBc01 )

	maya.cmds.text( label= line02 )
	cmdBc02 = uiModule + '.' + 'editTxtGrpButtonSelection("' + windowName + '_jointType' + '","textFieldButtonGrp")'
	maya.cmds.textFieldButtonGrp( windowName + '_jointType', label='Get Joint Type:', text='IK', buttonLabel='Select', en=True, bc=cmdBc02 )
	
	maya.cmds.text( label= line03 )
	cmdBc03 = uiModule + '.' + 'editTxtGrpButtonSelection("' + windowName + '_joints' + '","textFieldButtonGrp")'
	maya.cmds.textFieldButtonGrp( windowName + '_joints', label='Get Joints:', text='', buttonLabel='Select', en=True, bc=cmdBc03 )
	
	# Either replace existing groups in that are in the field be default be renaming them, selecting existing group nodes that
	# that meet the requirements or leaving them as default.
	txInField = 'char_GRP  DO_NOT_ALTER_GRP  skeleton_nonScale_GRP'
	maya.cmds.text( label= line04 )
	cmdBc04 = uiModule + '.' + 'editTxtGrpButtonSelection("' + windowName + '_groups' + '","textFieldButtonGrp")'
	maya.cmds.textFieldButtonGrp( windowName + '_groups', label='Get Groups:', text='', buttonLabel='Select', en=True, bc=cmdBc04, tx=txInField )
	

	maya.cmds.setParent('..')
	maya.cmds.setParent('..')
	maya.cmds.text( windowName + '_space1', label='' )
	maya.cmds.text( windowName + '_space2', label='' )
	
	cmdRun = thisModule + '.runWindow("' + windowName + '")'
	#maya.cmds.button(windowName + '_CreateSystem', label='Run Script', c='runWindow("' + windowName + '")' )
	maya.cmds.button(windowName + '_CreateSystem', label='Run Script', c=cmdRun)

	maya.cmds.showWindow( windowName )


# Run the functions	
def runWindow(windowName):
	getSidePrefix = maya.cmds.textFieldButtonGrp( windowName + '_sidePrefix', q=True, text=True )
	sp = getSidePrefix.split()
	sidePrefix = ''
	if(len(sp) > 0):
		sidePrefix = sp[0] + '_'

	getJointType = maya.cmds.textFieldButtonGrp( windowName + '_jointType', q=True, text=True )
	jt = getJointType.split()
	jointType = ''
	if(len(jt) > 0):
		jointType = jt[0] + '_'

	prefix = sidePrefix + jointType
	
	# Retrieve selected joints as a String value
	getJoints = maya.cmds.textFieldButtonGrp( windowName + '_joints', q=True, text=True )
	jointsArray = getJoints.split()
	
	# Retrieve selected groups as a String value
	getGroups = maya.cmds.textFieldButtonGrp( windowName + '_groups', q=True, text=True )
	groupsArray = getGroups.split()
	
	ikJoints = uRig.duplicateSelectedJoints(getJoints,getSidePrefix,getJointType,getGroups)

	
# Run the functions	
# injectThisModule : String This parameter is this module injected into the buildWindow function so that the runWindow function can be called correctly
def run(injectThisModule,injectUIModule):
	# Clears the old instance of the window is it exists.
	ui.deleteWindow(rebuildWindowName) 
	
	# 
	buildWindow(injectThisModule,injectUIModule,rebuildWindowName,windowTitle,line1,line2,line3,line4)
	
	
print("line 131 :: Imported uiRig_copySelectedJoints Module")