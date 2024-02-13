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
#	2. TODO
#	3. TODO
###############################################################################################


# Define local UI Variables
line1 = '	SELECT OBJECTS TO BASE GROUPS ON:-'
line2 = '	TYPE KEY NAME(s) OF GROUP(s) WITH SPACE BETWEEN:-'
line3 = '	(note: first grp name will be parent to second and so on)'

ver = ' : ver 01.001 ' # This needs to be updated each time the script is updated or modified.
windowTitle = 'Group Selected Nodes' + ver
rebuildWindowName = 'GroupSelectedNodes'


# Define local functions
	

def buildWindow(windowName,windowTitle, line01, line02, line03):
	questionButtonHeight=23
	maya.cmds.window( windowName, title= windowTitle, s=True, iconName='Short Name', widthHeight=(500, 300))
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
	#form = maya.cmds.formLayout(windowName + '_form1')
	#tabs = maya.cmds.tabLayout(windowName + '_tabs1', innerMarginWidth=5, innerMarginHeight=5)
	#maya.cmds.formLayout( form, edit=True, attachForm=[(tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)] )
	
	#maya.cmds.columnLayout('')
	#maya.cmds.scrollLayout('Global' , width=500, height=300, horizontalScrollBarThickness=16, verticalScrollBarThickness=16)

	maya.cmds.rowLayout(windowName + '_row2',numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn2=2, columnAlign2=('left','left'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
	
	maya.cmds.columnLayout(windowName + '_global1a', rs=3)
	maya.cmds.text( label= line01 )
	maya.cmds.textFieldButtonGrp( windowName + '_selection', label='Get Objects:', text='', buttonLabel='Select', en=True, bc='editTxtGrpButtonArray("' + windowName + '_selection' + '","textFieldButtonGrp")' )
	maya.cmds.text( label= line02 )
	maya.cmds.text( label= line03 )
	maya.cmds.textFieldButtonGrp( windowName + '_groups', label='Get GroupNames:', text='', buttonLabel='Select', en=True, bc='editTxtGrpButtonArray("' + windowName + '_groups' + '","textFieldButtonGrp")' )
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
	maya.cmds.button(windowName + '_CreateSystem', label='Run Script', c='runWindow("' + windowName + '")' )

	maya.cmds.showWindow( windowName )


# Run the functions	
def runWindow(windowName):
	getSel = maya.cmds.textFieldButtonGrp( windowName + '_selection', q=True, text=True )
	selectionArray = getSel.split()

	getGrp = maya.cmds.textFieldButtonGrp( windowName + '_groups', q=True, text=True )
	groupArray = getGrp.split()
	
	utl.createEmptyGroupFromObjMulti(selectionArray,groupArray)

	
# Run the functions	
def run():
	# Clears the old instance of the window is it exists.
	ui.deleteWindow(rebuildWindowName) 

	# 
	buildWindow(rebuildWindowName,windowTitle,line1,line2,line3)

print("line 0111 :: Imported uiRig_groupSelectedNodes Module")