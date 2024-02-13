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
line_01 = 'SELECT OBJECTS TO BASE GROUPS ON:-'
line_02 = 'TYPE KEY NAME(s) OF GROUP(s) WITH SPACE BETWEEN:-'
line_03 = '(note: first grp name will be parent to second and so on)'



ver = ' : ver 01.001 ' # This needs to be updated each time the script is updated or modified.
comment = 'Initial complete build of script.'
windowTitle = 'Create Empty Group Based On Object' + ver
rebuildWindowName = 'CreateEmptyGroupBasedOnObject'


textAlign = 'left'

# Define local functions
def buildWindow(thisModule,uiModule,windowName,windowTitle, line01, line02, line03):
	questionButtonHeight=23
	maya.cmds.window( windowName, title= windowTitle, s=True, iconName='Short Name', widthHeight=(500, 600))
	
	maya.cmds.frameLayout(  windowName + '_frameLayout1', label=' ', borderStyle="in", lv=False, bv=False, mw=10, mh=10)
	maya.cmds.columnLayout(windowName + '_column1', adjustableColumn=True)
	
	maya.cmds.text( label= '   ' )
	
	maya.cmds.rowLayout(windowName + '_row1',numberOfColumns=3, columnWidth3=(80, 80, 80), adjustableColumn3=3, columnAlign3=('left','left','left'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
	
	maya.cmds.text( label= '' )
	maya.cmds.text( label= '' )
	maya.cmds.text( label= '' )
	maya.cmds.setParent('..')
	
	maya.cmds.text( label= '   ' )
	
	maya.cmds.frameLayout(windowName + '_formBase', label='Tabs', lv=False, labelAlign='top', borderStyle='in')
	
	# Column 1 
	maya.cmds.columnLayout(windowName + '_column1', rowSpacing=1)
	
	maya.cmds.rowLayout( windowName + '_row1_1a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_descip1_1a', label= line01, height=questionButtonHeight, align=textAlign )
	maya.cmds.text( windowName + '_space1_1a', label='', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_2a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	cmdBc01 = uiModule + '.' + 'editTxtGrpButtonSelection("' + windowName + '_selection_2a' + '","textFieldButtonGrp")'
	maya.cmds.textFieldButtonGrp( windowName + '_selection_2a', height=questionButtonHeight, width=450, label='Get Objects:', text='', buttonLabel='Select', enable=True, buttonCommand=cmdBc01 )
	maya.cmds.button( windowName + '_help1_5a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	maya.cmds.columnLayout( windowName + '_column3a', rowSpacing=0 )
	maya.cmds.text( windowName + '_descip1_3a', label= line02, height=questionButtonHeight, align=textAlign )
	maya.cmds.text( windowName + '_descip1_3b', label=line03, height=questionButtonHeight, align=textAlign )
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_4a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	cmdBc04 = uiModule + '.' + 'editTxtGrpButtonSelection("' + windowName + '_selection_4a' + '","textFieldButtonGrp")'
	maya.cmds.textFieldButtonGrp( windowName + '_selection_4a', height=questionButtonHeight, width=450, label='Get Group Names:', text='', buttonLabel='Select', enable=True, buttonCommand=cmdBc04 )
	maya.cmds.button( windowName + '_help1_5a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	maya.cmds.text( windowName + '_space1_5a', label='' )
	maya.cmds.text( windowName + '_space1_5b', label='' )
	
	
	cmdRun = thisModule + '.runWindow("' + windowName + '")'
	maya.cmds.button(windowName + '_CreateSystem1_6a', label='Run Script', height=questionButtonHeight, width=470, command=cmdRun)
	
	
	maya.cmds.showWindow( windowName )


# Run the functions
def runWindow(windowName):
	getSel = maya.cmds.textFieldButtonGrp( windowName + '_selection_2a', q=True, text=True )
	selectionArray = getSel.split()

	getGrp = maya.cmds.textFieldButtonGrp( windowName + '_selection_4a', q=True, text=True )
	groupArray = getGrp.split()
	
	utl.createEmptyGroupFromObjMulti(selectionArray,groupArray)
	
	
	
# Run the functions	
# injectThisModule : String This parameter is this module injected into the buildWindow function so that the runWindow function can be called correctly
def run(injectThisModule,injectUIModule):
	# Clears the old instance of the window is it exists.
	ui.deleteWindow(rebuildWindowName) 
	
	# 
	buildWindow(injectThisModule,injectUIModule,rebuildWindowName,windowTitle,line_01,line_02,line_03)
	
	
print("line 162 :: Imported uiRig_createControlCurves Module")