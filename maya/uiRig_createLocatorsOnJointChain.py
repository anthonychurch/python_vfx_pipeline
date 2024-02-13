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
line1 = '	SELECT OBJECTS TO CREATE LOCATRS ON:-'
#line2 = '	TYPE KEY NAME(s) OF GROUP(s) WITH SPACE BETWEEN:-'
#line3 = '	(note: first grp name will be parent to second and so on)'

ver = ' : ver 01.001 ' # This needs to be updated each time the script is updated or modified.
windowTitle = 'Create Locators on Joint Chain' + ver
rebuildWindowName = 'CreateLocatorsOnJointChain'

# Define local functions


def buildWindow(thisModule,uiModule,windowName,windowTitle, line01):
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
	cmdBc01 = uiModule + '.' + 'editTxtGrpButtonSelection("' + windowName + '_selection' + '","textFieldButtonGrp")'
	#maya.cmds.textFieldButtonGrp( windowName + '_selection', label='Get Objects:', text='', buttonLabel='Select', en=True, bc='ui.editTxtGrpButtonArray("' + windowName + '_selection' + '","textFieldButtonGrp")' )
	maya.cmds.textFieldButtonGrp( windowName + '_selection', label='Get Objects:', text='', buttonLabel='Select', en=True, bc=cmdBc01 )
	
	#maya.cmds.text( label= line02 )
	#maya.cmds.text( label= line03 )
	#maya.cmds.textFieldButtonGrp( windowName + '_groups', label='Get GroupNames:', text='', buttonLabel='Select', en=True, bc='editTxtGrpButtonArray("' + windowName + '_groups' + '","textFieldButtonGrp")' )
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
	
	cmdRun = thisModule + '.runWindow("' + windowName + '")'
	#maya.cmds.button(windowName + '_CreateSystem', label='Run Script', c='runWindow("' + windowName + '")' )
	maya.cmds.button(windowName + '_CreateSystem', label='Run Script', c=cmdRun)

	maya.cmds.showWindow( windowName )


# Run the functions	
def runWindow(windowName):
	# Retrieve selection as a String value
	getSel = maya.cmds.textFieldButtonGrp( windowName + '_selection', q=True, text=True )
	# Convert String value to an Array to be injected into the function uRig.createLocatorsOnJointChain
	selectionArray = getSel.split()
	#print('uiRig_createLocatorsOnJointChain :: runWindow :: getSel = ' + str(getSel))
	print('uiRig_createLocatorsOnJointChain :: runWindow :: selectionArray = ' + str(selectionArray))
	parentLocators = True
	uRig.createLocatorsOnJointChain(selectionArray,parentLocators)

	
# Run the functions	
# injectThisModule : String This parameter is this module injected into the buildWindow function so that the runWindow function can be called correctly
def run(injectThisModule,injectUIModule):
	# Clears the old instance of the window is it exists.
	ui.deleteWindow(rebuildWindowName) 
	
	# 
	buildWindow(injectThisModule,injectUIModule,rebuildWindowName,windowTitle,line1)
	
	
print("line 118 :: Imported uiRig_createLocatorsOnJointChain Module")