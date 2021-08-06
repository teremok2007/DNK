import hou,sys
import os
import json
import sys
import re
lib_path = os.path.abspath('/studio/abc/users/bocharov/cooper/cooper/python')
sys.path.append(lib_path)
import cooper_data as cu_dat
import cooper_init
cu_proj=cooper_init.Cooper_Globals()['cooper_proj']












def apply_data( cur_node , version):
    
    cu_objects=[]
    res_obj=cur_node.parm('cu_data_name').eval()
    get_rule=cur_node.parm('cu_get_data_rule').eval()
    frame_format=cur_node.parm('cu_frame_format').eval()
    path=cur_node.parm('cu_data_path').eval()
    proj=path.split('/')[0]
    group=path.split('/')[1]
    #attrib_apply=cur_node.parm('apply_by_attr').eval()
    cu_mult_str=cur_node.parm('cu_multydata_keys').eval()

    ver_arr=[]
    cu_ver_str=''
    if version != 'NoVersion':
        ver_arr.append(version)
        cu_ver_str=str(ver_arr)
    else:
        cu_ver_str=str(ver_arr)

    objects_branches=res_obj.split('::')

    app_arr = cu_dat.ApplyData(group , proj , objects_branches[0] , objects_branches[1] , 'lv' , frame_format , 'Push_Ex' , cu_mult_str  ,  cu_ver_str  )



    g = cur_node.parmTemplateGroup()
    id = g.findIndices("cu_apply")

    for it in app_arr.keys():
        parm_name=it
        cur_parm = cur_node.parm(parm_name)

        if cur_parm == None:
        
           parameter = hou.StringParmTemplate(parm_name, parm_name,1)
           g.insertAfter(id, parameter)
           node.setParmTemplateGroup(g)
        

        cur_node.parm(parm_name).set(app_arr[it])
               
















scene=str(sys.argv[1])
rop_path=str(sys.argv[2])
time_slice=str(sys.argv[3])
current_frame = int(sys.argv[4])

hou.hipFile.load(scene)
ropnode=hou.node(rop_path)
render_range = (current_frame, current_frame, 1)





data_map=time_slice
data_update={}

list = hou.node('/').allSubChildren()
for i_node in list:
    if i_node.parm('cu_data_name'):
        data_name= i_node.parm('cu_data_name').eval()
        data_path=i_node.parm('cu_data_path').eval()
        
        data_map_file=cu_proj+str('/')+str(data_path)+str('/time_slice/')+str(data_map)
        if os.path.exists(data_map_file):
            dict={}
            with open(data_map_file) as json_data:
                dict = json.load(json_data)
            if data_name in dict['active_data']:
                data_update[data_name]=dict['active_data'][data_name]['create_version']
                i_node.parm("cu_get_data_rule").set('lv')
                print i_node.name()
                apply_data(i_node , dict['active_data'][data_name]['create_version'])
                
                
print "CU_DATA UPDATE:"
print data_update      



ropnode.render(frame_range=render_range)












































