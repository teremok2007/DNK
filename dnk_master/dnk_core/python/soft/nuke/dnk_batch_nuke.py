import cooper_data as cu_dat
import pyseq
import json
import nuke
import re
import os
import nukescripts
import re
import pyseq
import glob


def get_result_settings(proj_data , in_setting , data_box_name , de_rule ):
    dict_out={}
    in_sett_dict=json.loads(in_setting)

    init_cuper = cu_init.Cooper_Globals()  
    cu_proj = init_cuper['cooper_proj']
    data_path=str(cu_proj)+'/'+str(proj_data['ALL']['GROUP_DNK'].replace('::',''))+'/'+str(data_box_name)+'.dbox'
    dict_out={}

    dat={}
    with open(data_path) as f:
        dat = json.load(f)
    print dat
    if 'de_rule' in dat:
        if de_rule in dat['de_rule']:
            dict_out=dat['de_rule'][de_rule]
    
    for i in in_sett_dict.keys():
        dict_out[i]=in_sett_dict[i]

    return dict_out





def set_frame_range(file,node):
    print file
    files_arr=[]

    file_arr = re.split(r'%\d{2}d',file)
    if len(file_arr)<2:
        file_arr = re.split(r'\$F\d{1}',file)
        if len(file_arr)<2:
            file_arr = re.split(r'####',file)




    re_file = str(file_arr[0])+str('*')+str(file_arr[1])
    print re_file
    files_arr=glob.glob(re_file)
    if files_arr==[]:
        print '     File No Exist For Frame Range'
        return 0
    s = pyseq.Sequence(files_arr)

    #print s.format(format='%h%p%t %r %04l %m')
    start = s.format(format='%h%p%t %r').split(' ')[1].split('-')[0]
    end = s.format(format='%h%p%t %r').split(' ')[1].split('-')[1]
    
    node['first'].setValue(int(start))
    node['last'].setValue(int(end))
    node['origfirst'].setValue(int(start))
    node['origlast'].setValue(int(end))
    








def apply_batch( node_in , in_proj_data , time_slice_data):


    node=node_in




    res_obj=node.knob('result_data').value()
    get_rule=node.knob('version_info').value()
    proj_data=in_proj_data

    set_str=str(node.knob('set').value())
    set_dict=json.loads(str(node.knob('set').value()))



    #####____GET_VERSION_FROM_ATTR___IF VER_EXIST____
    if 'v' in set_dict:
        set_dict['v']=get_rule
        set_str=json.dumps(set_dict)
    if 'set' in set_dict:
        node.knob('cu_info').setValue(json.dumps(set_dict['set'].keys()))


        
    re_rule=str(node.knob('re_rule').value())

    attrib_mode=node.knob('cu_mode').value()
    multy_data_str=node.knob('cu_info').value()

    version_str_in=node.knob('version_info').values()

    version_str_in.remove('vld')
    version_str_in.remove('lv')
    version_str=str(version_str_in)

    objects_branches=res_obj.split('::')

    fin_sett=get_result_settings(proj_data , set_str , res_obj , re_rule )

    ####_________def ApplyData( proj_data , dbox_name ,dbox_brache , version_rule , frame_format , app_mode , multydata_str , version_str)_________
    app_arr = cu_dat.ApplyData(proj_data , res_obj , fin_sett['b'] , fin_sett['v'] , fin_sett['f'] ,  attrib_mode , multy_data_str , version_str)
    #print fin_sett

    get_set_setting=fin_sett['set']

    create_node={}

    for i_key in get_set_setting.keys():
        file_node=get_set_setting[i_key]
        create_node[i_key]=[file_node.split('.')[0],file_node.split('.')[1]]

    #print create_node



        


    cu_objects=[]




    n_x=node.knob("xpos").value()
    n_y=node.knob("ypos").value()


    bw=120
    node.knob("bdwidth").setValue(bw)
    i=0
    a=0
    arr=0
    for it in app_arr.keys():
        if it not in create_node:
            print 'This Key Not Exist'
            continue
        if create_node[it][0] !='':
            node_name=create_node[it][0]
        else:
            node_name=str(node.name())+'_'+str(res_obj)+"_"+it
        my_node=nuke.toNode(node_name)

        if my_node == None:
            
            if attrib_mode=='Get':
                my_node=nuke.createNode('Read')
                set_frame_range( app_arr[it] , my_node)
            else:
                my_node=nuke.createNode('Write')

        if attrib_mode=='Get':

            set_frame_range( app_arr[it] , my_node)



        my_node['name'].setValue(node_name)
        
            
        nw=my_node.width()
        nh=my_node.height() 
        my_node.knob("xpos").setValue(n_x+20+i)
        my_node.knob("ypos").setValue(n_y+50)
            
        i=i+120
        a=a+1
        if (my_node.knob(create_node[it][1])!=None):
            my_node.knob(create_node[it][1]).setValue(app_arr[it])    
        arr=arr+1
       
    node.knob("bdwidth").setValue(bw*a)


            
    