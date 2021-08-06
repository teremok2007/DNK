import os

lib_path = os.path.abspath('/studio/abc/users/bocharov/cooper/cooper/python')
sys.path.append(lib_path)

import cooper_init

import json
import sys
import nuke
cu_proj=cooper_init.Cooper_Globals()['cooper_proj']

import cooper_data as cu_dat
import re
import nukescripts






def apply_data(node_applay_name , version):

    cu_objects=[]
    node=nuke.toNode(node_applay_name)


    res_obj=node.knob('result_data').value()
    get_rule=node.knob('get_data_rule').value()
    frame_format=node.knob('frame_format').value()
    proj=node.knob('proj').value()
    group=node.knob('group_name').value()
    attrib_apply=node.knob('apply_by_attr').value()
    cu_mult_str=node.knob('cu_info').value()
    
    ver_arr=[]
    cu_ver_str=''
    if version != 'NoVersion':
        ver_arr.append(version)
        cu_ver_str=str(ver_arr)
    else:
        cu_ver_str=str(ver_arr)

    objects_branches=res_obj.split('::')


    app_arr = cu_dat.ApplyData(group , proj , objects_branches[0] , objects_branches[1] , 'lv' , frame_format , 'Push_Ex' , cu_mult_str  ,  cu_ver_str  )
    print app_arr






    cu_objects=[]





    n_x=node.knob("xpos").value()
    n_y=node.knob("ypos").value()


    bw=120
    node.knob("bdwidth").setValue(bw)
    i=0
    a=0
    for it in app_arr.keys():
        node_name=str(node.name())+'_'+str(res_obj)+"_"+it
        my_node=nuke.toNode(node_name)

        if my_node == None:
        
 
            my_node=nuke.createNode('Read')
            my_node['name'].setValue(node_name)
            my_node['first'].setValue(1001)
            my_node['last'].setValue(1100)
            nw=my_node.width()
            nh=my_node.height() 
            my_node.knob("xpos").setValue(n_x+20+i)
            my_node.knob("ypos").setValue(n_y+50)
        
        i=i+120
        a=a+1
        if (my_node.knob(attrib_apply)!=None):
            my_node.knob(attrib_apply).setValue(app_arr[it])    
   
    node.knob("bdwidth").setValue(bw*a)


        
    










scene=str(sys.argv[1])
frame=int(sys.argv[2])
write_node=str(sys.argv[3])
data_map=str(sys.argv[4])


nuke.scriptOpen(scene)
data_update={}

for i in nuke.allNodes():
    if i.knob('is_data_get') != None:

        data_name=i.knob('result_data').value()
        #data_name=re.sub('::','',data_name)

        data_proj=i.knob('proj').value()
        data_group=i.knob('group_name').value()
        data_map_file=cu_proj+str('/')+str(data_proj)+str('/')+str(data_group)+str('/time_slice/')+str(data_map)
        
        if os.path.exists(data_map_file):
            #print "Data Map Exist"
            dict={}
            with open(data_map_file) as json_data:
                dict = json.load(json_data)
            if data_name in dict['active_data']:
                data_update[data_name]=dict['active_data'][data_name]['create_version']
                i.knob('get_data_rule').setValue('lv')

                #print "EXEC"
                apply_data(i.name() , dict['active_data'][data_name]['create_version'])
        else:
            #data_update.append(data_name)
            #i.knob('get_data_rule').setValue('lv')
            print "NO_EXEC"
            #apply_data(i.name() , dict['active_data'][data_name]['create_version'])

print "CU_DATA UPDATE:"
print data_update 

    



  
nuke.execute(write_node , frame, frame)




