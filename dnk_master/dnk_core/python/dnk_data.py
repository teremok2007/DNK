from pyseq import pyseq
#import pyseq
import os 
import glob
import re
import json
from DNK.dnk_master.dnk_core.python.dnk_utils import dnk_init as cu_init


def reslash(a):
    b=[]
    for i in a:
        #print i
        ii=i.replace('\\','/')
        b.append(ii)
    return b

def GetSequenceFileRecursion(in_array,out_array,a):
        
        names = in_array[:]        
        names.sort()

        if (a==None):
                a=0
        else:
                if (a!=len(names)):
                        del names[0:a]
                else:

                        return out_array

        s = pyseq.Sequence(names)        
        #out_array.append( s.format(format='%h%p%t %R %04l %m ') )
        my_form ='%h%p%t'
        out_array.append( s.format(my_form) )

        a=a+len(s)
        GetSequenceFileRecursion(in_array,out_array,a)






def GetDataRecursion( out , all_files , pattern , rule_parts , it , rule_parts_len):


    if it==(rule_parts_len-1):
        

        out_files=[]
        out_files_pattern_in = glob.glob(pattern)
        out_files_pattern=reslash(out_files_pattern_in)

        if (len(out_files_pattern)!=0):
            for out_it in out_files_pattern:
                out_files.append(out_it)
            out.append(out_files)

        return out
    
    else:

        files_pattern_in = glob.glob(pattern)
        files_pattern=reslash(files_pattern_in)
        up_it=it+1
        

        if len(files_pattern)!=0:
            for i in files_pattern:
                up_pattern=str(i)+str('/')+str(rule_parts[up_it])
                GetDataRecursion( out , all_files , up_pattern , rule_parts , up_it , rule_parts_len)

                  





def re_version(version_arr , rule_get , mode , data_dict):
	out=''
	if mode == 'Push' or mode == 'push':
		version_arr.sort()
		out_v=version_arr[-1]
		padding=len(out_v)
		current_version=str(int(out_v)+1)
		out=current_version.zfill(padding)

	elif mode == 'Push_Ex':
		out=version_arr[0]



	elif mode == 'Get' or mode == 'get':

		if rule_get=='vld':
			if 'valid_version' in data_dict:
				out=data_dict['valid_version']
			else:
				out='NO_VALID'
		elif rule_get=='lv':
			version_arr.sort()
			out=version_arr[-1]
		else:
			out=rule_get
	return out







def re_frame(frame_inj,fr_rule):

	fr_out='%04d'
	if fr_rule=='hou':
		fr_out='$F4'
	elif fr_rule=='nk':
		fr_out='%04d'
	elif fr_rule=='ma':
		fr_out='####'   	
	return fr_out




def GetDataBox( rule , proj_data ):
	####PREPARE DATA RULE - SET PROJECT VARIABLES
	r1 = re.compile(r'<<[^>>]+>>') 
	pr = re.findall(r1,rule)
	
	for ipr in pr:
		replace_prepare=str(ipr).replace('<<','')
		replace_prepare=str(replace_prepare).replace('>>','')
		rule=rule.replace(str(ipr),str(proj_data['ALL'][replace_prepare][0]))


	#print rule




















	out_warn=''








	data_out={}
	rules={}
	rule_divide=[]

	r1 = re.compile(r'{{[^}}]+}}') 
	a = re.findall(r1,rule)

	num=0

	for i in a:
		preitem=re.sub('{{','',i)
		item=re.sub('}}','',preitem)

		if re.search('V', item):
			rules[num]=item

		elif re.search('F', item):
			rules[num]=item

		elif re.search('B', item):
			rules[num]=item

		elif re.search('M', item):
			rules[num]=item


		rule=re.sub(i,'*',rule)
 	
		num=num+1


	rule_divide=rule.split("*")
	


	#print rule_divide
	#print rules
	#print rule
	rule=rule+str('*')
	it=0

	out=[]

	all_files_in = glob.glob(rule)
	all_files=reslash(all_files_in)


	if all_files == None :
		out_warn=out_warn+'NO_DATA'+'\n'
		#print 'NO_DATA'
	#print all_files
	rule_output = []
	rule_atom_str = "/"
	### WINDOWS###################
	if os.name=='nt':
		rule_atom_str = ""
	##############################
	rule_input = rule.split('/')

	for rule_it in rule_input:
		if (rule_it.find("*")!=-1):

			rule_atom_str=str(rule_atom_str)+str(rule_it)

			rule_output.append(rule_atom_str)
			rule_atom_str=""
		else:
			rule_atom_str=str(rule_atom_str)+str(rule_it)+str('/')




	rule_parts = rule_output

	rule_parts_len=len(rule_parts)

	pattern=str(rule_parts[it])




	GetDataRecursion( out , all_files , pattern , rule_parts , it , rule_parts_len)
	out.sort()

	version_dict={}
	multy_data_dict={}
	branches_dict={}

	version_array=[]
	multy_data_array=[]
	branches_array=[]
	data_array=[]
	for data in out:
		data_no_path=[]
		for iter in data:
			data_no_path_str=iter.split('/')
			data_no_path.append(data_no_path_str[-1])

        
        
    
        
		data_str=data[0]
		dir_file=os.path.dirname(data_str)
		out_sequence_array=[]

		GetSequenceFileRecursion(data_no_path,out_sequence_array,None)

		for it_seq in out_sequence_array:

			out_str=str(dir_file)+str('/')+str(it_seq)

			rule_left_part=rule_divide[0]
			rule_div_len=len(rule_divide)

			branch_str=':'
			multy_data_dict.setdefault(branch_str, {})
			version_dict.setdefault(branch_str, {})

			for it_rule in range(0,rule_div_len-1):

				current_rule=rules[it_rule]
				divideExp=str(rule_divide[it_rule+1])
				if str(divideExp)=='.':
					divideExp=re.sub('.','\.',divideExp)

				re_rule=str(rule_left_part)+'(.*?)'+str(divideExp)
				res = re.search(re_rule, out_str)
				rule_left_part=str(rule_left_part)+str(res.group(1))+str(rule_divide[it_rule+1])

				if re.search('B', current_rule):
					branch_str=branch_str+'/'+str(res.group(1))

					multy_data_dict.setdefault(branch_str, {})
					version_dict.setdefault(branch_str, {})


				elif re.search('V', current_rule):
					version_dict[branch_str][str(res.group(1))]=current_rule

				elif re.search('M', current_rule):
					#print str(res.group(1))
					multy_data_dict[branch_str][str(res.group(1))]=current_rule

	        	

		
			data_array.append(out_str)

			branches_dict[branch_str]=0
#			print "DICT:"
#			print branches_dict
#			print multy_data_dict
#			print version_dict
	
	for key in branches_dict:
		branches_array.append(key)


	brance_out_dict	= {}

	for arr_it in branches_array:
		
		ver_dict=version_dict[arr_it]
		multy_dict=multy_data_dict[arr_it]
		pre_out_dict={}
		
		pre_out_dict['V'] = list(ver_dict.keys())
		pre_out_dict['M'] = list(multy_dict.keys())

	
		brance_out_dict[arr_it]=pre_out_dict

	data_out['D']=data_array
#	data_out['V']=version_array
	data_out['B']=brance_out_dict
#	data_out['M']=multy_data_array
	data_out['_rules_']=rules
	data_out['_rules_divide_']=rule_divide
#	print "OUT"
	#print data_out

	return data_out











def GetData(data_box , data_box_dict , currrent_branche, rule_get_data , frame_format_rule , mode  , multydata_arr , version_arr ):

	out_data={}
	currrent_branche=str(':')+currrent_branche
	#in_D =data_box['D']
	in_V = []
	in_M = []

	in_B = data_box['B']

	if in_B=={} and mode=='Push':
		in_V = version_arr
		in_M = multydata_arr
	else:
		if in_B=={}:
			in_V = version_arr
			in_M = multydata_arr
		else:
			in_V =data_box['B'][currrent_branche]['V']
			in_M = data_box['B'][currrent_branche]['M']

	if mode=='Push_Ex':
		in_V = version_arr


	in_rules_arr = data_box['_rules_']
	in_str_divide_arr = data_box['_rules_divide_']
	
	
	if len(in_M)==0:
		in_M.append('simple')

	cur_branche_arr=currrent_branche.split("/")


	#print "ARR_LEN"
	#print len(cur_branche_arr)

	
	for it_m in in_M:
		cur_br=1
		rule_left_part=in_str_divide_arr[0]
		rule_div_len=len(in_str_divide_arr)

		for it_rule in range(0,rule_div_len-1):

			current_rule=in_rules_arr[it_rule]

 		
			if re.search('B', current_rule):
				rule_left_part=str(rule_left_part)+str(cur_branche_arr[cur_br])+str(in_str_divide_arr[it_rule+1])
				cur_br=cur_br+1
			if re.search('V', current_rule):
				version=re_version( in_V, rule_get_data ,mode ,data_box_dict)
				rule_left_part=str(rule_left_part)+str(version)+str(in_str_divide_arr[it_rule+1])
			if re.search('F', current_rule):
				frame=re_frame( current_rule , frame_format_rule )
				rule_left_part=str(rule_left_part)+str(frame)+str(in_str_divide_arr[it_rule+1])
			if re.search('M', current_rule):
				rule_left_part=str(rule_left_part)+str(it_m)+str(in_str_divide_arr[it_rule+1])
		out_data[it_m]=rule_left_part


	return out_data
		










def GetObjects(proj_data ,mode):

	init_cuper=cu_init.Cooper_Globals() 
	#print 'PROOOOOOOJ'
	#print proj_data
	directory_name=init_cuper['cooper_proj']+str('/')+proj_data['ALL']['GROUP_DNK'].replace('::','')
#	out_data_object={}
	out_obj=[]
	out_keys={}

	os.chdir(directory_name)
	for file in glob.glob("*.dbox"):
		dir_and_file=directory_name+'/'+file
		file_only=re.sub('.dbox','',file)
		with open(dir_and_file) as f:
			data_file = json.load(f)

		rule=data_file['rule']
		out_pre_data={}
		out_pre_data=GetDataBox(rule , proj_data)



		#print "MY_DATA"
		#print out_pre_data
		str_out_br =''

		if out_pre_data['B']=={} and mode=='Push':
			#print "None Branche"
			br_string_init=''
			mult_arr_init=[]
			ver_arr_init=[]
			for rule_it in list(out_pre_data['_rules_'].keys()):
				if re.search('B', out_pre_data['_rules_'][rule_it]):
					br_string_init=br_string_init +'/'+ '__init__'
				elif re.search('M', out_pre_data['_rules_'][rule_it]):
					mult_arr_init.append('__init__')
				elif re.search('V', out_pre_data['_rules_'][rule_it]):
					ver_arr_init.append('0000')									

			str_out_br=str(file_only)+'::'+str(br_string_init) +'::Keys::'+ str(mult_arr_init)+'::Keys::'+str(ver_arr_init)
			out_obj.append(str_out_br)

		else:
			#print "Branche"
			
			for br_it in list(out_pre_data['B'].keys()):
				str_out_br=str(file_only)+':'+str(br_it) +'::Keys::'+ str(out_pre_data['B'][br_it]['M'])+'::Keys::'+str(out_pre_data['B'][br_it]['V'])

				out_obj.append(str_out_br)

	out_obj.sort()

#		out_data_object[file_only]=[out_obj,out_keys]
	

	return out_obj
	











def UpdateObjects( proj_data , mode , data_name):

	init_cuper=cu_init.Cooper_Globals() 
	directory_name=init_cuper['cooper_proj']+str('/')+proj_data['ALL']['GROUP_DNK'].replace('::','')
#	out_data_object={}
	out_obj=[]
	out_keys={}

	os.chdir(directory_name)
	for file in glob.glob("*.dbox"):
		dir_and_file=directory_name+'/'+file
		file_only=re.sub('.dbox','',file)
		with open(dir_and_file) as f:
			data_file = json.load(f)

		rule=data_file['rule']
		out_pre_data={}
		out_pre_data=GetDataBox( rule , proj_data )



		#print "MY_DATA"
		#print out_pre_data
		str_out_br =''

		if out_pre_data['B']=={} and mode=='Push':
			#print "None Branche"
			br_string_init=''
			mult_arr_init=[]
			ver_arr_init=[]
			for rule_it in list(out_pre_data['_rules_'].keys()):
				if re.search('B', out_pre_data['_rules_'][rule_it]):
					br_string_init=br_string_init +'/'+ '__init__'
				elif re.search('M', out_pre_data['_rules_'][rule_it]):
					mult_arr_init.append('__init__')
				elif re.search('V', out_pre_data['_rules_'][rule_it]):
					ver_arr_init.append('0000')									

			str_out_br=str(file_only)+'::'+str(br_string_init) +'::Keys::'+ str(mult_arr_init)+'::Keys::'+str(ver_arr_init)
			out_obj.append(str_out_br)

		else:
			#print "Branche"
			
			for br_it in list(out_pre_data['B'].keys()):
				str_out_br=str(file_only)+':'+str(br_it) +'::Keys::'+ str(out_pre_data['B'][br_it]['M'])+'::Keys::'+str(out_pre_data['B'][br_it]['V'])

				out_obj.append(str_out_br)

	out_obj.sort()

	date_slice=''
	date_out=''
	for date_it in out_obj:
		date_slice=date_it.split('::Keys::')[0]
		if date_slice==data_name:
			date_out=date_it
			break
	
	#print date_out
	return date_out























def ApplyData( proj_data , obj_name , cur_brache , get_data_rule , frame_format , app_mode , multydata_str , version_str):




	init_cuper = cu_init.Cooper_Globals() 
	directory_name = init_cuper['cooper_proj']+str('/')+proj_data['ALL']['GROUP_DNK'].replace('::','')
	#print cur_brache
	

	multydata_arr = eval(multydata_str)
	version_arr = eval(version_str)

	out_res=[]

	in_file = directory_name+'/'+str(obj_name)+str('.dbox')
	with open(in_file) as f:
		data_file = json.load(f)
	rule = data_file['rule']
	out_data = {}
	out_data = GetDataBox(rule , proj_data)


	out_res = GetData(out_data , data_file , cur_brache, get_data_rule , frame_format , app_mode , multydata_arr , version_arr )

	return out_res




def SimpleApplyData( proj_data , obj_name ):

	out_res = ''

	return out_res



def FrameRangeFromDataBox( proj_data , obj_name):

	out_res = ''

	return out_res