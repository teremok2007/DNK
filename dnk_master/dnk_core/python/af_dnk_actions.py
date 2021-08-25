from __future__ import with_statement
import sys
from DNK.dnk_master.dnk_core.python.dnk_utils import dnk_init as cu_init
import time
import json



#cgru_lib='R:/06_Tools/Revo/cgru.3.2.0.windows/cgru.3.2.0/afanasy/python/'
#lib_path = os.path.abspath(cgru_lib)
#sys.path.append(lib_path)


import dnk_utilities as util
import os
import af

###################################Utility##############################

employess={}
sheets={}
data_map={}
data_map.setdefault('active_data', {})
data_map.setdefault('path', '')
##############################_TaskRecursiveFunctions_##################################

def recursionTask(job,mynode,depth,maskObject,employess, data_map , in_time , sheet_in, iterator):

    name=mynode.split('/')[-1].split('.')[0]
    node_path=mynode.replace(mynode.split('/')[-1],'')
    data_atom_map={}

    mynode_data={}
    with open(mynode) as f:
        mynode_data = json.load(f)    

    data_map.setdefault('active_data', {})

    out_nodes=mynode_data['outputs']
    """    
    for depit in out_nodes:
        if (depit.knob('is_data')!=None):
            if mynode.knob('disable').value()==False:

                data_name=util.re_script(depit.knob('data_name').value() ,depit, sheet_in, iterator )
                data_proj = str(util.re_script(depit.knob('proj').value() ,depit, sheet_in, iterator ))
                data_group = str(util.re_script(depit.knob('group_name').value() ,depit, sheet_in, iterator ))

                data_box_get=cu_data.UpdateObjects(data_group,data_proj,'Get',data_name)
                version_arr=eval(data_box_get.split('::Keys::')[2])
                cur_version=''
                if version_arr !=[]:
                    cur_version=cu_data.re_version(version_arr , 'lv' , 'Push' , {})
                else:
                    cur_version='NoVersion'
                data_dict={}
                data_dict['create_version']=cur_version
                data_map['active_data'][data_name]=data_dict
                data_map['path']=str(data_proj)+'/'+str(data_group)


    """

    af_parm={}

    if ('af_parm' in mynode_data):
        
        af_parm=mynode_data['af_parm']




    block = af.Block( name )

    if 'hostmask' in af_parm:
        block.setHostsMask(str(af_parm['hostmask']))
    if 'hostmaskexclude' in af_parm:
        block.setHostsMaskExclude(str(af_parm['hostmaskexclude']))
    """
    if mynode.knob("data_map") :
        mynode.knob("data_map").setValue(in_time)


    if mynode.knob("af_service") :
        service_name=mynode.knob("af_service").value()
        block.setService(service_name)
    """
    if 'frame_range' in mynode_data:

        startin=str(mynode_data['frame_range'][0])
        endin=str(mynode_data['frame_range'][1])
        
  
        start=str(util.re_attribute( startin , mynode , str("node") , sheet_in, iterator ))
        end=str(util.re_attribute( endin , mynode , str("node") , sheet_in, iterator ))
 
        print(start)
        if int(start)>int(end):
            end=start


        cmd=''
        if mynode_data['disable']==1:
            task = af.Task('ThisDisabled')
            cmd = ''
            task.setCommand( cmd )
            block.tasks.append( task )
        else:

            for iter in range(int(start),int(int(end)+1)):

                task = af.Task('It %d' % ( iter ) )

                cmd = util.get_command( mynode , iter , sheet_in, iterator )             
                #cmd=mynode_data['command']
                init_cuper = cu_init.Cooper_Globals()

                #########___Add_Data_Map_Attribute___####################
                data_map_dir = str(iterator) +'/_time_slice_/'
                data_map_file=data_map_dir+in_time
                cmd=cmd+' '+data_map_file
                #########################################################

                task.setCommand( cmd )
                block.tasks.append( task )
 
               

    else:
         cmd=mynode_data['command']
         cmd = util.get_command(mynode,0 , sheet_in, iterator)  
         block.setCommand(cmd)



    ###### GET RECURSIVE INPUT NODE ########
    inputs=mynode_data['inputs']

    mask=''
    
    for it in inputs:
        
        nodeIn=node_path+it+'.doit'
        print(nodeIn)
        node_d={}
        if os.path.exists(nodeIn):
            with open(nodeIn) as f:
                node_d = json.load(f) 


        if node_d!={} and node_d['command']!=None:

            if maskObject!=None:

                if ( it in maskObject):
                             
                    mask+= str(it)+'|'
                    recursionTask(job,nodeIn,0,maskObject,employess,data_map , in_time , sheet_in, iterator)
            else:
                mask+= str(it)+'|'
                recursionTask(job,nodeIn,0,maskObject,employess,data_map , in_time , sheet_in, iterator)

    block.setDependMask(mask)
    employess[name]=block









def reverseRecursionTask(mynode,depth,employess):
    print("")
    node_data={}
    with open(mynode) as f:
        node_data = json.load(f)
    employess[mynode.split('/')[-1].split('.')[0]]=depth
    depth=depth+1
    dep=node_data['outputs']

    moni_path=mynode.replace(mynode.split('/')[-1] , '')
	
    for it in dep:
        node_full_path=str(moni_path)+str(it)+str('.doit')
        if os.path.exists(node_full_path):
            reverseRecursionTask(node_full_path,depth,employess)




def getTime():
    t=time.time()
    return str(t)

"""

#################################Mains################################
def runSelectDownStream(iterate):
    employess={}
    sheet={}
    init_cuper = cu_init.Cooper_Globals()
    data_map={}
    in_time=getTime()

    job=af.Job('JOB')
    
    nodeA=nuke.selectedNode()
    name=nodeA.name()
    
    maskObj=None
    recursionTask(job,nodeA,0,maskObj,employess,data_map,in_time,sheet,iterate)
    #print employess
    for key in employess:
        a=employess[key]
        print a
        job.blocks.append(a)


    if data_map.get('path')!=None:
        data_map_file=init_cuper['cooper_proj'] + '/' + data_map['path']+'/time_slice/'+in_time
        data_map_dir=init_cuper['cooper_proj'] + '/' + data_map['path']+'/time_slice/'
        if not os.path.exists(data_map_dir):
            os.makedirs(data_map_dir)

        print data_map_file
        with open(data_map_file, "w") as write_file:
            json.dump(data_map, write_file)
    
    job.send()
"""




def runSelectUpStream(iterate , doit_node , sheet_all ):


    #fp = open('R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper_tmp/temp.txt', 'w')
    #fp.write(str(doit_node))
    init_cuper = cu_init.Cooper_Globals()
    data_map={}
    in_time=getTime()
    sheet=sheet_all
    employess={}
    nodes=[]


    moni_path=doit_node.replace(doit_node.split('/')[-1] , '' )

    sys.stdout.flush()
    

    job=af.Job(str(iterate)+'::'+str(in_time))
    

    nodes.append(doit_node)


    for cur_node in nodes:
        reverseRecursionTask(cur_node ,0, employess)
    employessOut=[]


    for key in sorted(employess, key = lambda x: int(employess[x]),reverse = True):
        a=key,employess[key]
        employessOut.append(a[0])

    node_start=str(moni_path)+(employessOut[0])+str('.doit')

    employess={}
    
    recursionTask( job,node_start , 0 , employessOut , employess , data_map , in_time , sheet , iterate )

 
    for key in employess:
        a=employess[key]

        job.blocks.append(a)

    data_map_dir =init_cuper['cooper_proj'] + '/' + str(iterate) +'/_time_slice_/'
    data_map_file=data_map_dir+in_time
    
    if not os.path.exists(data_map_dir):
        os.makedirs(data_map_dir)


    with open(data_map_file, "w") as write_file:
        json.dump(data_map, write_file)

    
    #fp.write(str(employess))
    #fp.close()
    #return 1  
    #job.setUserName('philipp.bye')
    job.send()
    





"""


def runSelectNodes(iterate, doit_nodes, proj_data ):


    nodes=doit_nodes

    for node in nodes:

        util.compille(node)
        name=node.name()

        job=af.Job(name)


        hostmask=node.knob("hostmask").value()
        hostmaskexclude=node.knob("hostmaskexclude").value()


        
        
        block = af.Block( name , hostmask )
        block.setHostsMask(hostmask)
        block.setHostsMaskExclude(hostmaskexclude)

        if node.knob("af_service") :
            service_name=node.knob("af_service").value()
            block.setService(service_name)

        if node.knob("usecounter").value() :

            startin=node.knob("start").value()
            endin=node.knob("end").value()
            

            start=util.re_script( startin , node , sheet_in, iterate )
            end=util.re_script( endin , node , sheet_in, iterate )

            
            for iter in range(int(start),int(int(end)+1)):
                task = af.Task('It %d' % ( iter ) )
                cmd = util.get_command( node , iter )
                task.setCommand( cmd )
                block.tasks.append( task )
                   
        else:
             
            cmd = util.get_command(node,0)  
            block.setCommand(cmd)
        job.blocks.append( block )
        job.send()




def printTask(task):
    strA=str('custom.durationStart("')+str(task)+str('")')
    print strA
    eval(strA)


"""






    
