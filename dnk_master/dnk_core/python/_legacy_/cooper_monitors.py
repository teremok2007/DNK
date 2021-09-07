import os

#cooper_libs =os.environ['COOPER_LIBS']
#cooper_libs ='/studio/abc/users/bocharov/cooper/cooper/python/'
#lib_path = os.path.abspath(cooper_libs)
#sys.path.append(lib_path)


from DNK.dnk_master.dnk_core.python.dnk_utils import dnk_init as cu_init

import json
import re



def where_am_i(input_path_str):

	out={}            

	data_dict={}
	group_rule=[]
	project_str=[]

	init_cuper = cu_init.Cooper_Globals() 
	proj_json = init_cuper['cooper_proj']

	data_file={}
	proj_dirs=os.listdir(proj_json)
	
	for pr_it in proj_dirs:
		init_proj_json=proj_json+'/'+pr_it+'/'+'_init_'
		#print init_proj_json
		if os.path.exists(init_proj_json):
			with open(init_proj_json) as f:
				data_file = json.load(f)
			#print data_file


			in_str_arr=input_path_str.split('/')

			group_mask = data_file['group_mask']
			group_rule = data_file['group_rule']

			project_str=data_file['dnk_project_structure']
			#print project_str
			#print group_mask

			for mask_it in group_mask:

				arr_d={}

				mask_arr = mask_it.split('/')
				strOut=''

				for it_msk in range(0,len(mask_arr)):
					arr_data_dict=[]
					#print it_msk
					#print len(in_str_arr)
					if (len(in_str_arr)-1)<it_msk:
						#print "In string lenght less current group mask"
						data_dict={}
						break
					strOut=strOut+in_str_arr[it_msk]+'/'

					if str(in_str_arr[it_msk])!=str(mask_arr[it_msk]):
						#print "No matches and... "

						r1= re.compile(r'{{[^}}]+}}') 
						a=re.findall(r1,mask_arr[it_msk])
						if a==[] and it_msk<(len(mask_arr)-1):
							#print "Input string part NO matches group mask part BREAK"
							#print in_str_arr
							#print mask_arr[it_msk]
							data_dict={}
							break
						else:
							#print "This Expression"
							for i in a:
								preitem=re.sub('{{','',i)
								item=re.sub('}}','',preitem)
								arr_data_dict.append(in_str_arr[it_msk])
								arr_data_dict.append(strOut)
								data_dict[item]=arr_data_dict
								arr_data_dict=[]
					else:
						print("Input string part MATCHES group mask part ")





	#print data_dict

	if data_dict=={}:
		out['PRJ']="NotFound"
		out['GROUP']="NotFound"
		out['ALL'] = {}
		return out

	#print "DataDict"
	#print data_dict
	#print "Recovery PROJ/GROUP info"
    
	pre_out_arr=[]

	for rec_it in group_rule:
        
		r1= re.compile(r'{{[^}}]+}}') 
		a=re.findall(r1,rec_it)

		for i in a:
			preitem=re.sub('{{','',i)
			item=re.sub('}}','',preitem)
			pre_out=data_dict[item][0]
			rec_it=re.sub(i, pre_out , rec_it ) 
		pre_out_arr.append(rec_it) 

	aa=0
	group_find=data_dict[project_str[0]][0]+str('::')
	for pr_it in project_str:
		aa=aa+1
		if aa==1:
			continue
		group_find=str(group_find)+'/'+str(data_dict[pr_it][0])

	data_dict['GROUP_DNK']=group_find


	out['PRJ']=pre_out_arr[0]
	out['GROUP']=pre_out_arr[1]
	out['ALL'] = data_dict



	#print out
	return out





def get_proj_data(input_proj_str):
	out={}            

	data_dict={}
    
	group_rule=[]
    
    
	init_cuper = cu_init.Cooper_Globals() 
	proj_json = init_cuper['cooper_proj']

	data_file={}
	proj_init_file=str(proj_json)+str('/')+str(input_proj_str)+'/'+'_init_'
	

	if os.path.exists(proj_init_file):
		with open(proj_init_file) as f:
			data_file = json.load(f)
	
	return data_file


def get_user_data():
	out={}            

	data_dict={}
    
	group_rule=[]
    
    
	init_cuper = cu_init.Cooper_Globals() 
	user_json = init_cuper['cooper_user']

	data_file={}
	proj_init_file=str(user_json)+str('/')+'_init_'
	

	if os.path.exists(proj_init_file):
		with open(proj_init_file) as f:
			data_file = json.load(f)
	
	return data_file




def proj_data_recovery(proj_data):
    proj_arr=proj_data.split('/')
    proj_data_dict=get_proj_data(proj_arr[0])
    
    dnk_project_structure=proj_data_dict['dnk_project_structure']
    dict_out={}
    a=0
    for i in dnk_project_structure:
        dict_out[i]=proj_arr[a]
        a=a+1
    
    return dict_out