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
line_01 = 'USE THE FOLLOWING BUTTONS TO CREATE CURVE CONTROLS:'
line_02 = 'THE RIGGING COLOUR STANDARDS ARE AS FOLLOWS:'
line_03 = 'ARRAY KEY ARE 0=Left, 1=Right, 2=Centre, 3=Misc'
line_04 = 'THE MAYA NODE "overrideColor" ATTRIBUTES VALUES ARE:'
line_05 = ' 1. IKcolour = [14,13,17]'
line_06 = ' 2. FKColour = [23,31,25]'
line_07 = ' 3. splineIKColour = [6,15,29]'
line_08 = ' 4. clothColour = [9,30,21]'
line_09 = ' 3. faceColour = [22,10,26]'
line_10 = ' 4. misc = [4,7,11]'
line_11 = 'GIVE A NAME TO THE CURVE CONTROL:'
line_12 = 'PICK A SOLVER TYPE: IK,  FK,  SplineIK,  Cloth,  Face,  OR  Misc:'
line_14 = 'PICK A SIDE PREFIX: Left,  Right,  Centre, OR  Misc:'


ver = ' : ver 01.006 ' # This needs to be updated each time the script is updated or modified.
comment = 'Initial complete build of script.'
windowTitle = 'Create Control Curves for Rigs' + ver
rebuildWindowName = 'CreateCtrlCrvsRigging'

# Define Rigging Colour Standards
# 0=Right, 1=Left, 2=Centre, 3=Misc
IKcolour = [14,13,17]
FKcolour = [23,31,25]
splineIKcolour = [6,15,29]
clothColour = [9,30,21]
faceColour = [22,10,26]
misc = [4,7,11]

solverTypesColours = [IKcolour,FKcolour,splineIKcolour,clothColour,faceColour,misc]

axis = "y"
scale = 1

textAlign = 'left'

# Define local functions
def buildWindow(thisModule,uiModule,windowName,windowTitle, line01, line02, line03, line04, line05, line06, line07, line08, line09, line10, line11):
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
	#maya.cmds.rowLayout(windowName + '_row2',numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn2=2, columnAlign2=('left','left'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
	#maya.cmds.rowColumnLayout(windowName + '_row2', numberOfColumns=2,columnWidth=[(1,450),(2,20)])
	
	# Column 1 
	maya.cmds.columnLayout(windowName + '_column1', rowSpacing=1)
	
	maya.cmds.rowLayout( windowName + '_row1_1a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_descip1_1a', label= line02, height=questionButtonHeight, align=textAlign )
	maya.cmds.text( windowName + '_space1_1a', label='', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_2a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_descip1_2a', label= line03, height=questionButtonHeight, align=textAlign )
	maya.cmds.button( windowName + '_help1_2a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_3a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_space1_3a', label='' )
	maya.cmds.text( windowName + '_space1_3b', label='' )
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_4a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_descip1_4a', label= line04, height=questionButtonHeight, align=textAlign )
	maya.cmds.button( windowName + '_help1_4a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	maya.cmds.rowLayout( windowName + '_row1_5a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_descip1_5a', label= line05, height=questionButtonHeight, align=textAlign )
	maya.cmds.button( windowName + '_help1_5a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_6a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_descip1_6a', label= line06, height=questionButtonHeight, align=textAlign )
	maya.cmds.button( windowName + '_help1_6a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_7a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_descip1_7a', label= line07, height=questionButtonHeight, align=textAlign )
	maya.cmds.button( windowName + '_help1_7a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_8a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_descip1_8a', label= line08, height=questionButtonHeight, align=textAlign )
	maya.cmds.button( windowName + '_help1_8a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_9a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_descip1_9a', label= line09, height=questionButtonHeight, align=textAlign )
	maya.cmds.button( windowName + '_help1_9a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_10a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_descip1_10a', label= line10, height=questionButtonHeight, align=textAlign )
	maya.cmds.button( windowName + '_help1_10a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_11a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_space1_11a', label='' )
	maya.cmds.text( windowName + '_space1_11b', label='' )
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_12a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	maya.cmds.text( windowName + '_descip1_12a', label= line11, height=questionButtonHeight, align=textAlign )
	maya.cmds.text( windowName + '_space1_12a', label='' )
	maya.cmds.setParent('..')
	
	
	maya.cmds.rowLayout( windowName + '_row1_14a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left'))
	#name = maya.cmds.textField( windowName + '_name1_14a', height=questionButtonHeight )
	#maya.cmds.text( windowName + '_space1_14a', label='' )
	name_crv = windowName + '_name1_14a'
	name = maya.cmds.textField( name_crv, height=questionButtonHeight, width=450 )
	maya.cmds.setParent('..')
	
	
	# Radio buttons for selecting the prefix
	maya.cmds.columnLayout( windowName + '_column2', rowSpacing=1 )
	maya.cmds.text( windowName + '_descip1_15a', label=line_12, height=questionButtonHeight, align=textAlign )
	maya.cmds.rowLayout( windowName + '_row1_15a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left') )
	#solverType = maya.cmds.textField( windowName + '_solverType1_15a', height=questionButtonHeight, placeholderText='IK', width=450 )
	#maya.cmds.button( windowName + '__help1_15a', label='?', height=questionButtonHeight)
	maya.cmds.rowColumnLayout( windowName + '_rowColumn1_15a', numberOfColumns=6 )
	#collection_solverTypes = maya.cmds.radioCollection( windowName + '_collection_solverTypes1_15a' )
	name_solverTypes = windowName + '_collection_solverTypes1_15a'
	collection_solverTypes = maya.cmds.radioCollection( name_solverTypes )
	st1 = maya.cmds.radioButton( 'ik', label='IK' )
	st2 = maya.cmds.radioButton( 'fk', label='FK' )
	st3 = maya.cmds.radioButton( 'splineik', label='SplineIK' )
	st4 = maya.cmds.radioButton( 'cloth', label='Cloth' )
	st5 = maya.cmds.radioButton( 'face', label='Face' )
	st6 = maya.cmds.radioButton( 'misc', label='Misc' )
	maya.cmds.radioCollection( collection_solverTypes, edit=True, select=st1 )
	maya.cmds.setParent('..')
	maya.cmds.button( windowName + '__help1_15a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	# Radio buttons for selecting the colour based on the prefix
	maya.cmds.columnLayout( windowName + '_column3', rowSpacing=1 )
	maya.cmds.text( windowName + '_descip1_16a', label=line_14, height=questionButtonHeight, align=textAlign )
	maya.cmds.rowLayout( windowName + '_row1_16a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left') )
	maya.cmds.rowColumnLayout( windowName + '_rowColumn1_16a', numberOfColumns=4 )
	#collection_sidePrefix = maya.cmds.radioCollection( windowName + '_collection_sidePrefix1_16a' )
	name_sidePrefix = windowName + '_collection_sidePrefix1_16a'
	collection_sidePrefix = maya.cmds.radioCollection( name_sidePrefix )
	sp1 = maya.cmds.radioButton( '_left', label='Left' )
	sp2 = maya.cmds.radioButton( '_right', label='Right' )
	sp3 = maya.cmds.radioButton( '_centre', label='Centre' )
	sp4 = maya.cmds.radioButton( '_misc', label='Misc', enable=False )
	maya.cmds.radioCollection( collection_sidePrefix, edit=True, select=sp3 )
	maya.cmds.setParent('..')
	maya.cmds.button( windowName + '__help1_16a', label='?', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	# Column 3 - Description for buttons
	maya.cmds.rowLayout( windowName + '_row1_17a', numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn=1, columnAlign=(1, 'left') )
	maya.cmds.text( windowName + '_descip1_17a', label= line01, height=questionButtonHeight, align=textAlign )
	maya.cmds.text( windowName + '_space1_17a', label='', height=questionButtonHeight)
	maya.cmds.setParent('..')
	
	
	# Button Create Square Arrow Ctrl
	#maya.cmds.columnLayout(windowName + '_column2', rowSpacing=1)
	#maya.cmds.rowLayout(windowName + '_column2')
	maya.cmds.rowColumnLayout(windowName + '_column2', numberOfRows=1)
	arg_createSquareArrowCtrl = [solverTypesColours, name_crv, name_solverTypes, name_sidePrefix, axis, scale]
	#cmdRun_createSquareArrowCtrl = thisModule + '.runCreateSquareArrowCtrl("' + windowName + '",' + '"y"' + ',' + str(scale) + ')'
	cmdRun_createSquareArrowCtrl = thisModule + '.runCreateSquareArrowCtrl(' + str(arg_createSquareArrowCtrl) + ')'
	maya.cmds.button( windowName + '_CreateSquareArrowCtrl', label='Run Create Square Arrow Ctrl', command=cmdRun_createSquareArrowCtrl )
	# Column 4 - Button Create Diamond Stand Ctrl
	#maya.cmds.rowColumnLayout(windowName + '_column2', numberOfRows=1)
	arg_createDiamondStandCtrl = [solverTypesColours, name_crv, name_solverTypes, name_sidePrefix, axis, scale]
	cmdRun_createDiamondStandCtrl = thisModule + '.runCreateDiamondStandCtrl(' + str(arg_createDiamondStandCtrl) + ')'
	maya.cmds.button( windowName + '_CreateDiamondStandCtrl', label='Run Create Diamond Stand Ctrl', command=cmdRun_createDiamondStandCtrl )

	
	#s = maya.cmds.radioCollection( collection_solverTypes, query=True, select=True )
	
	maya.cmds.showWindow( windowName )


# Run the functions
#def runCreateSquareArrowCtrl(windowName,colour,axis,scle):
#def runCreateSquareArrowCtrl( windowName, axis, scle ):
def runCreateSquareArrowCtrl( args ):
	tempName = '_temp_name_'
	colArray = args[0]
	nmeField = args[1]
	typeField = args[2]
	sideField = args[3]
	axis = args[4]
	scle = args[5]
	#print tempName
	
	getName = maya.cmds.textField( nmeField, q=True, text=True )
	if not getName:
		getName = tempName
	print "getName = " + str(getName) + "\n"
	
	getSolverType = maya.cmds.radioCollection( typeField, query=True, select=True )
	print "getSolverType = " + str(getSolverType) + "\n"
	
	getPrefix = maya.cmds.radioCollection( sideField, query=True, select=True )
	getPrefix = getPrefix[1:len(getPrefix)]
	print "getPrefix = " + str(getPrefix[1:len(getPrefix)]) + "\n"
	
	colour = runGetColour(colArray,getSolverType,getPrefix)
	print "colour = " + str(colour) + "\n"
	
	getName = runGetName(getName,getSolverType,getPrefix)
	
	uCrv.createSquareArrowCtrl(getName,colour,axis,scle)
	

def runCreateDiamondStandCtrl( args ):
	tempName = '_temp_name_'
	colArray = args[0]
	nmeField = args[1]
	typeField = args[2]
	sideField = args[3]
	axis = args[4]
	scle = args[5]
	
	getName = maya.cmds.textField( nmeField, q=True, text=True )
	if not getName:
		getName = tempName

	getSolverType = maya.cmds.radioCollection( typeField, query=True, select=True )
	
	getPrefix = maya.cmds.radioCollection( sideField, query=True, select=True )
	getPrefix = getPrefix[1:len(getPrefix)]
	
	colour = runGetColour(colArray,getSolverType,getPrefix)
	
	getName = runGetName(getName,getSolverType,getPrefix)
	
	uCrv.createDiamondStandCtrl(getName,colour,axis,scle)


def runGetColour(stc, gs, gp):
	type = 0
	if(gs == 'ik'):
		type = 0
	elif(gs == 'fk'):
		type = 1
	elif(gs == 'splineik'):
		type = 2
	elif(gs == 'cloth'):
		type = 3
	elif(gs == 'face'):
		type = 4
	elif(gs == 'misc'):
		type = 5

	prefx = 0
	if(gp == 'left'):
		prefx = 0
	elif(gp == 'right'):
		prefx = 1
	elif(gp == 'centre'):
		prefx = 2
	elif(gp == 'misc'):
		prefx = 4
	
	arrCol = stc[type]
	print "type = " + str(type) +"/n"
	print "prefx = " + str(prefx) +"/n"
	print "gs = " + str(gs) +"/n"
	print "gp = " + str(gp) +"/n"
	
	return arrCol[prefx]		


def runGetName(nme, gs, gp):
	type = 'IK_'
	if(gs == 'ik'):
		type = 'IK_'
	elif(gs == 'fk'):
		type = 'FK_'
	elif(gs == 'splineik'):
		type = 'SpIK_'
	elif(gs == 'cloth'):
		type = 'CLTH_'
	elif(gs == 'face'):
		type = 'FCE_'
	elif(gs == 'misc'):
		type = 'MISC_'

	prefx = 'L_'
	if(gp == 'left'):
		prefx = 'L_'
	elif(gp == 'right'):
		prefx = 'R_'
	elif(gp == 'centre'):
		prefx = 'C_'
	elif(gp == 'misc'):
		prefx = 'M_'
		
	return prefx + type + nme + '_1'
	
	
# Run the functions	
# injectThisModule : String This parameter is this module injected into the buildWindow function so that the runWindow function can be called correctly
def run(injectThisModule,injectUIModule):
	# Clears the old instance of the window is it exists.
	ui.deleteWindow(rebuildWindowName) 
	
	# 
	buildWindow(injectThisModule,injectUIModule,rebuildWindowName,windowTitle,line_01,line_02,line_03,line_04,line_05,line_06,line_07,line_08,line_09,line_10,line_11)
	
	
print("line 162 :: Imported uiRig_createControlCurves Module")