from __future__ import with_statement

import re
import os
import sys
import dnk_init
import subprocess
import json

#import custom

#GOOGLE





def in_dictionary(key, dict):
    if key in dict:
        return True
    return False








def re_script( txt , node , sheet , sheet_it):
    err=''



    name=node.split('/')[-1].split('.')[0]
    node_path=node.replace(node.split('/')[-1],'')
    data_atom_map={}

    mynode_data={}
    with open(node) as f:
        mynode_data = json.load(f)    
    


    itemval=''
    r1= re.compile(r'<<[^>>]+>>')
    a=re.findall(r1,txt)
    txtOut=txt    

    for i in a:
        preitem=re.sub('<<','',i)
        item=re.sub('>>','',preitem)


        if (item in mynode_data['in']):

            itemval=re_attribute(str(mynode_data['in'][item]), node , str("node"), sheet , sheet_it)

        else:
            #### FIND GROUP _init_ NODE ####################################################
            shot_init_file = node_path + '/_init_'
            ################################################################################
            if os.path.exists(shot_init_file):
                shot_node_data={}
                with open(shot_init_file) as f:
                    shot_node_data = json.load(f)
                if item in shot_node_data['in']:
                    itemval=re_attribute(str(shot_node_data['in'][item]), shot_init_file , str("dropnode"), sheet , sheet_it )
                
            else:
                ### FIND PROJ _init_ NODE ################################################
                print (' Attr Not Fount in GROUP _init_ File --> Find in PROJ _init_ file')
                init=dnk_init.Cooper_Globals()
                cu_proj_path=init['cooper_proj']+'/'
                cu_proj_path=cu_proj_path.replace('//','/')
                prj_path=cu_proj_path + node_path.replace(cu_proj_path,'').split('/')[0]
                prj_ini_node = prj_path+'/_init_'
                ##########################################################################
                itemval=re_attribute(str(i), prj_ini_node , str("dropnode"), sheet , sheet_it )



        txtOut=re.sub(i,itemval , txtOut )

    return txtOut




def re_attribute( in_text , nodeb , mode , sheet , sheet_it):
    err=''
    name=nodeb.split('/')[-1].split('.')[0]
    node_path=nodeb.replace(nodeb.split('/')[-1],'')
    data_atom_map={}

    mynode_data={}
    with open(nodeb) as f:
        mynode_data = json.load(f)    
    
    r1= re.compile(r'<<[^>>]+>>') 
    a=re.findall(r1,in_text)
    
    out_text=in_text

    itemval=''
    for i in a:
        preitem=re.sub('<<','',i)
        item=re.sub('>>','',preitem)

        if re.search('\.', item):
            print('FIND DOT')

            if re.search(':', item):
                sheet_data=item.split(".")
                sheet_name_node=sheet_data[0]
                sheet_row=sheet_data[1].split(":")[0]
                sheet_collumn=sheet_data[1].split(":")[1]

                if sheet_collumn=='':
                    sheet_collumn=sheet_it

                #itemval = re_sheet_attribute( sheet_name_node , sheet , sheet_row ,  int(sheet_collumn))
                itemval = sheet[sheet_name_node][sheet_collumn][sheet_row]
                #with open('R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper_tmp/data.json', 'w') as f:
                    #json.dump(sheet_name_node, f , indent=4)
            else:

                one_node_name=item.split(".")[0]
                one_node_knob=item.split(".")[1]

                one_node=node_path + one_node_name +'.doit'
                if os.path.exists(one_node):
                        one_node_data={}
                        with open(one_node) as f:
                            one_node_data = json.load(f) 

                        if one_node_knob in one_node_data['in']:
                
                            itemval=re_attribute(str(one_node_data['in'][one_node_knob]), one_node , str("node"), sheet , sheet_it)
                        else:
                            err='No Attribute'

                else:
                    err='No Node'



        else:

            if mode == "node" :
                #### FIND GROUP _init_ NODE ####################################################
                shot_init_file = node_path + '/_init_'
                ################################################################################
                if os.path.exists(shot_init_file):
                    shot_node_data={}
                    with open(shot_init_file) as f:
                        shot_node_data = json.load(f)


                    if item in shot_node_data['in']:
                        itemval=re_attribute(str(shot_node_data['in'][item]), shot_init_file , str("dropnode"), sheet , sheet_it )
                    else:
                        ### FIND PROJ _init_ NODE################################################
                        print (' Attr Not Fount in GROUP _init_ File --> Find in PROJ _init_ file')
                        init=dnk_init.Cooper_Globals()
                        cu_proj_path=init['cooper_proj']+'/'
                        cu_proj_path=cu_proj_path.replace('//','/')
                        prj_path=cu_proj_path + node_path.replace(cu_proj_path,'').split('/')[0]
                        prj_ini_node = prj_path+'/_init_'
                        #########################################################################
                        itemval=re_attribute(str(i), prj_ini_node , str("dropnode"), sheet , sheet_it )



                else:
                    ### FIND PROJ _init_ NODE################################################
                    print ('GROUP _init_ File Not Fount --> Find in PROJ _init_ file')
                    init=dnk_init.Cooper_Globals()
                    cu_proj_path=init['cooper_proj']+'/'
                    cu_proj_path=cu_proj_path.replace('//','/')
                    prj_path=cu_proj_path + node_path.replace(cu_proj_path,'').split('/')[0]
                    prj_ini_node = prj_path+'/_init_'
                    
                    #########################################################################
                    itemval=re_attribute(str(i), prj_ini_node , str("dropnode"), sheet , sheet_it )



            else: #mode == "dropnode" :
            #### GET ARRT FROM PROJ _init_ FILE #####
                
                init=dnk_init.Cooper_Globals()
                cu_proj_path=init['cooper_proj']+'/'
                cu_proj_path=cu_proj_path.replace('//','/')

                prj_path=cu_proj_path + node_path.replace(cu_proj_path,'').split('/')[0]

                prj_ini_node = prj_path+'/_init_'
                print(prj_ini_node)
                if os.path.exists(prj_ini_node):

                    prj_node_data={}
                    with open(prj_ini_node) as f:
                        prj_node_data = json.load(f)
                    if item in prj_node_data['in']:
                        itemval=prj_node_data['in'][item]
                    else:
                        
                        print('Attr Not Fount in PROJ _init_ File --> Set Attr -1')
                        itemval='-1'
                else:
                    
                    print ('PROJ _init_ File Not Fount --> Set Attr -1')
                    itemval='-1'


        out_text=re.sub(i,itemval , out_text )

    return out_text






def re_frame(txt,fr):

    r1= re.compile(r'<<FF[^>>]+>>') 
    a=re.findall(r1,txt)
    #print a
    txtOut=txt
    for i in a:
        preitem=re.sub('<<FF','',i)
        item=re.sub('>>','',preitem)        
        padding = int(item)
        frame = fr
        txt = "%0*d" % (padding, frame) 
        txtOut=re.sub(i,txt , txtOut )    
    return txtOut



def re_iterator(txt,iterator):

    r1= re.compile(r'<<PP[^>>]+>>') 
    a=re.findall(r1,txt)

    txtOut=txt
    for i in a:
        txt = str(iterator) 
        txtOut=re.sub(i,txt , txtOut ) 
         
    return txtOut


def get_command( node , fra , sheet_in, iterator):
    
    nodename=node.split('/')[-1].split('.')[0]
    node_path=node.replace(node.split('/')[-1],'')
    data_atom_map={}
    mynode_data={}
    with open(node) as f:
        mynode_data = json.load(f)
    multilineTextInput=''
    multilineTextOutput=''
    
    if 'command' in mynode_data:
        
        comm=str(mynode_data['command'])
        multilineTextInput = comm

        multilineTextOutput=re_iterator(multilineTextInput,iterator) 
        multilineTextOutput=re_frame(multilineTextOutput,fra) 
 
        multilineTextOutput=re_script(multilineTextOutput,node, sheet_in, iterator)

     
    return multilineTextOutput

'''
def compille(node, sheet_in, iterator):

    message=str("Compile-")+str(node.name())
    #print message
    nodename=node.name()
    val=str(node.knob("scriptname").value())

    ext=str(node.knob("extention").value())
    if (val==""):
        message=str("Error : Script Name Not Found\nCompile Stop\n\n\n")
        #print message 
        return 0

    fileName=str(node.knob("scriptlocation").value())
    if os.path.exists(fileName):
        message=str("Directory-    \"")+str(fileName)+str("\"     Found")
        #print message
    else:
        message=str("Directory-    \"")+str(fileName)+str("\"     Not Found\nCompile Stop\n\n\n")
        #print message
        return 0


    fileLoc=str(node.knob("scriptlocation").value())+str("/compile/")+str(iterator)
    fileName+=str("/")+val+str('.prescr')
    fileOutName=val

    fileCuperScriptDir=os.path.dirname(__file__)
	

    if os.path.exists(fileName):
        message=str("File-    \"")+str(fileName)+str("\"     Found")
        #print message
    else:
        message=str("File-    \"")+str(fileName)+str("\"     Not Found\n\tUse Predifened Directory - \"../cooper/scripts\"")
        #print message
        fileCuperScriptDir=re.sub("cooper/python","cooper/scripts" , fileCuperScriptDir )  
        fileName=fileCuperScriptDir+str("/")+val+str('.prescr')
        if os.path.exists(fileName):
            message=str("File-    \"")+str(fileName)+str("\"     Found")
            #print message
        else:
            message=str("File-    \"")+str(fileName)+str("\"     Not Found\nCompile Stop\n\n\n")
            #print message
            return 0
        
    
    if os.path.exists(fileLoc):
        message=str("OutPath-    \"")+str(fileLoc)+str("\"     Found")
        #print message
    else:
        #print 'CreateDir'
        #print fileLoc
        os.mkdir(fileLoc) 

    fOutLoc=fileLoc+str("/")+fileOutName+str("_")+str(nodename)+str(".")+str(ext)
    
    f=open(fileName, 'r')
    fOut=open(fOutLoc, 'w')
    multilineTextInput = str(f.read())
    multilineTextOutput=re_script( multilineTextInput , node , sheet_in, iterator )
    fOut.write(multilineTextOutput)
    f.close()
    fOut.close()
    #print "Compile Successfully\n\n\n"
'''
