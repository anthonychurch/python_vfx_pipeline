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
#	SELECT:	
#	1. SELECT THE ALL ADDITIONAL CLAW JOINTS FROM THE START TO END
#	2. SELECT roll_LOC
#	3. MAIN CONTROL
###############################################################################################


# Define local UI Variables
line1 = '	SELECT OBJECTS TO BE CONSTRAINED:-'
line2 = '	SELECT OBJECTS TO DRIVE CONSTRAINT:-'
line3 = '	SELECT SELECT TYPE OF CONSTRAINT:-'

ver = ' : ver 01.001 ' # This needs to be updated each time the script is updated or modified.
windowTitle = 'Contrain Selected Objects' + ver
rebuildWindowName = 'contrainSelectedObjects'


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
	maya.cmds.textFieldButtonGrp( windowName + '_drivers', label='Get Driver Objects:', text='', buttonLabel='Select', en=True, bc='editTxtGrpButtonArray("' + windowName + '_drivers' + '","textFieldButtonGrp")' )
	maya.cmds.text( label= line03 )
	maya.cmds.radioButtonGrp( windowName + '_constraintType', label='Constraint Type:', labelArray3=['parent', 'point', 'aim'], numberOfRadioButtons=3, en=True, sl=1 )
	maya.cmds.text( label= '' )
	maya.cmds.checkBoxGrp(windowName + '_offset', numberOfCheckBoxes=1, label='Offset', value1=True)
	#maya.cmds.text( label= line3 )
	maya.cmds.setParent('..')

	maya.cmds.columnLayout(windowName + '_global1b', rs=3)
	maya.cmds.text( label= '   ' )
	maya.cmds.button(label='?', height = questionButtonHeight)
	maya.cmds.text( label= '   ' )
	maya.cmds.button(label='?', height = questionButtonHeight)
	maya.cmds.text( label= '   ' )
	maya.cmds.setParent('..')
	
	maya.cmds.setParent('..')
	#maya.cmds.setParent('..')
	#maya.cmds.setParent('..')

	maya.cmds.text( windowName + '_space1', label='' )
	maya.cmds.text( windowName + '_space2', label='' )
	maya.cmds.button(windowName + '_CreateSystem', label='Run Script', c='runWindow("' + windowName + '")' )

	maya.cmds.showWindow( windowName )


def runWindow(windowName):
	getSel = maya.cmds.textFieldButtonGrp( windowName + '_selection', q=True, text=True )
	selection = getSel.split()

	getDrivers = maya.cmds.textFieldButtonGrp( windowName + '_drivers', q=True, text=True )
	drivers = getDrivers.split()

	getType = maya.cmds.radioButtonGrp( windowName + '_constraintType', q=True, sl=True )
	type = utl.whichConstaintType(getType)

	offset = maya.cmds.checkBoxGrp( windowName + '_offset', q=True, value1=True )

	#sel = maya.cmds.radioButtonGrp( windowName + '_selection', q=True, sl=True )
	#selection = whichAxis(fra)[1]
	#jua = maya.cmds.radioButtonGrp( windowName + '_jointUpAxis', q=True, sl=True )
	#pitchAxis = whichAxis(jua)[1]
	#jra = maya.cmds.radioButtonGrp( windowName + '_jointRotAxis', q=True, sl=True )
	#rotateAxis = whichAxis(jra)[1]

	#print ('rollAxis = ' + str(rollAxis) )
	#print ('rotateAxis = ' + str(rotateAxis) )
	#print ('pitchAxis = ' + str(pitchAxis) )
	
	uRig.contraints = setupConstrainSelection(drivers,selection,type,offset)


# Run the functions	
def run():
	# Clears the old instance of the window is it exists.
	ui.deleteWindow(rebuildWindowName) 

	# 
	buildWindow(rebuildWindowName,windowTitle,line1,line2,line3)

print("line 0130 :: Imported uiRig_constrainSelected Module")