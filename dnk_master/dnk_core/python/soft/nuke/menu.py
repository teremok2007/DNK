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

import nuke
lib_path = os.path.abspath('/studio/abc/users/bocharov/cooper/cooper/python')
sys.path.append(lib_path)
import af_cooper_actions
import cooper_init as cu_init
cu_init.Set_Proxy()






cu_init.Nuke_Menu()