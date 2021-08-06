

##### vol.01 - EXPORT_ABC_ASMBL ########


import os
import sys
import shutil
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import pymel.core as pm
import re
import glob
import time
import cooper_monitors as cu_moni
import cooper_init as cu_init
import pyseq
import string

import RevoProc as rvpr
import RevoAssemble as revo_asmbl




    
in_time_slice=sys.argv[1]
proj_data_input=in_time_slice.split('_time_slice_')[0]


prj=proj_data_input.split('/')[1]
seq=proj_data_input.split('/')[2]
group_in=proj_data_input.split('/')[3]

proj_data=cu_moni.get_proj_data(prj)

filename=proj_data['real_proj_dir'][0]+'/'+prj+'/'+'production/sequence/'+seq+'/'+group_in+'/layout/ma/'+group_in+'_layout.ma'
print filename
cmds.file( filename, o=True , f=True )


    
revo_asmbl.export_assemble_abc()









