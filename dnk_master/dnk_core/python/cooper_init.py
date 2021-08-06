import os
def Set_Proxy():

	return 1






def Nuke_Menu():


	import nuke
	cu_toolbar = nuke.menu('Nodes')

	cooper = cu_toolbar.addMenu('DNK', icon='mcIcon.png')
	cooper.addCommand('Data Box', 'nuke.nodePaste("R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/gizmos/GetData.nk")')
	cooper.addCommand('Abstract', 'nuke.nodePaste("R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/gizmos/Abstract.nk")')

	actionsmenu=cooper.addMenu('Actions', icon='mcIcon.png')
	actionsmenu.addCommand('->>Run', 'af_cooper_actions.runSelectDownStream(-1)')
	actionsmenu.addCommand('Run->>', 'af_cooper_actions.runSelectUpStream(-1)')
	actionsmenu.addCommand('RunSelect', 'af_cooper_actions.runSelectNodes()')

	pipemenu=cooper.addMenu('Pipeline', icon='mcIcon.png')
	mayamenu=cooper.addMenu('Maya', icon='mcIcon.png')
	houdinimenu=cooper.addMenu('Houdini', icon='mcIcon.png')
	nukemenu=cooper.addMenu('Nuke', icon='mcIcon.png')
	shellmenu=cooper.addMenu('Shell', icon='mcIcon.png')
	custommenu=cooper.addMenu('CustomCommand', icon='mcIcon.png')




	#houdinimenu.addCommand('HoudiniEvalNode', 'nuke.nodePaste("/studio/proj/temp/cooper/gizmos/houdini/Houdini_eval_node.nk")')
	maya_atommenu=mayamenu.addMenu('Atoms', icon='mcIcon.png')
	maya_atommenu_mel=maya_atommenu.addMenu('Mel', icon='mcIcon.png')
	maya_atommenu_py=maya_atommenu.addMenu('Python', icon='mcIcon.png')


	hou_atommenu=houdinimenu.addMenu('Atoms', icon='mcIcon.png')
	hou_atommenu.addCommand('_atom_refresh_attribute_', 'nuke.nodePaste("R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/gizmos/houdini/atoms/_hou_refresh_attribute_.nk")')

	nuke_atommenu=nukemenu.addMenu('Atoms', icon='mcIcon.png')




	pipemenu.addCommand('DaliesCreate', 'nuke.nodePaste("R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/gizmos/pipe/dalies_create.nk")')
	pipemenu.addCommand('FolderCreate', 'nuke.nodePaste("R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/gizmos/pipe/create_folder.nk")')

	houdinimenu.addCommand('HoudiniRender', 'nuke.nodePaste("R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/gizmos/houdini/Houdini_render.nk")')
	houdinimenu.addCommand('HoudiniSimulation', 'nuke.nodePaste("R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/gizmos/houdini/Houdini_simulation.nk")')
	houdinimenu.addCommand('HoudiniCheperdaRender', 'nuke.nodePaste("R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/gizmos/houdini/Houdini_Cheperda_Render.nk")')


	nukemenu.addCommand('NukeRender', 'nuke.nodePaste("R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/gizmos/nuke/Nuke_render.nk")')



def DNK_Globals():
	init = {}
	init['cooper_proj']      = 'R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper_proj/'
	init['studio_proj']      = 'R:/01_Projects/'
	init['cooper_user']      = 'R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper_users/'
	init['cooper_tmp']       = 'R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper_tmp/'
	init['cooper_python']    = 'R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/python/'
	init['cooper_scripts']   = 'R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/scripts/'
	init['credentials_file'] = 'R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/python/revo-tech-studio-db2297c4ea3d.json'
	init['CGRU_LOCATION']    = 'R:/06_Tools/Revo/cgru.3.2.0.windows/cgru.3.2.0/'
	init['run_projects']     = [ 'Dog' ]
	return init
