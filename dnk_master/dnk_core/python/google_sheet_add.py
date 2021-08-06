import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	
import json
from sys import argv
import cooper_init as cu_init
import cooper_monitors as cu_moni
import string
import google_sheet_get as ggl_get
import os


def recursion_list( y , gl_str ,dnk_struct , depth , res , arr ):
    res=res+'/'+y
    if depth==(len(dnk_struct)-1):
        #print('ASD')
        arr.append(res)
        return 1

    smask=gl_str[0]+'/'+str(y)+'/'+gl_str[1]
    #print(smask)
    depth=depth+1
    
    xx=dnk_struct[depth]
    gl_strr=smask.split(str('{{'+xx+'}}'))
     
    list=os.listdir(gl_strr[0])

    for yyy in list:
        if yyy[0]=='_':
            continue

        #print(os.path.isdir(str(gl_strr[0]+'/'+yyy)))
        if os.path.isdir(str(gl_strr[0]+'/'+yyy)):
            recursion_list( yyy, gl_strr ,dnk_struct, depth , res, arr )








def createAlphabetDict(iter):
    off=0
    d={}
    ch=[]
    for i in range(1,iter):
        for n, ch in (enumerate(string.ascii_uppercase)):        
            d[n+off]=ch*i
        off=off+26  
    return d






def add_collumns_sheets( proj_data_in , list_name , row_name , in_array ):

    proj=proj_data_in.split('/')[1]

    init_cuper = cu_init.Cooper_Globals()
    CREDENTIALS_FILE =init_cuper['credentials_file']

    proj_data=cu_moni.get_proj_data(proj)

    sheet_id=proj_data['google_id_map'][proj]

    alpha=createAlphabetDict(10)
    spreadsheetId=sheet_id

    print (spreadsheetId)

    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http()) 
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) 

    sheet_in=ggl_get.get_sheets( proj_data_in)
    id_arr=[]
    for i in sheet_in['main'].keys():
        id_arr.append(sheet_in['main'][i]['id'])
    #data=sheet['main']['/Dog/abc/abc_0040']
    id_arr.sort()
    max_id=id_arr[-1]+1
    end_id=max_id+len(in_array)
    range_string=str(list_name)+str('!')+str(row_name)+str(max_id)+str(':')+str(row_name)+str(end_id)
    
    body_in={}
    data=[]    
    small_body={}

    collumn=[]
    
    for arr in in_array: 
        row=[]
        row.append(arr)
        collumn.append(row)
    small_body['range']=range_string
    small_body['majorDimension']='ROWS'
    small_body['values']=collumn
    data.append(small_body)
    body_in['valueInputOption']='USER_ENTERED'
    body_in['data']=data


    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body =body_in ).execute()













    ##################### _list_###################__v__########__h__##############
    #result_from_google_sheet=results['sheets'][0]['data'][0]['rowData'][0]['values'][1]['formattedValue']
    

    return 1
    

######_EXAMPLE_####################

init=cu_init.Cooper_Globals()



cu_proj    = init['cooper_proj']
studio_proj= init['cooper_proj']
run_proj   = init['run_projects']

arrr=[]
for i in run_proj:
    my_proj=cu_moni.get_proj_data(i)
    dnk_struct=my_proj['dnk_project_structure']
    mask=str(my_proj['group_mask'][0])
    maask=mask.replace(str('{{'+dnk_struct[0]+'}}'), i)
    aa=dnk_struct[1]
    gl_str=maask.split(str('{{'+aa+'}}'))
    res='/'+i
    list=os.listdir(gl_str[0])
    #print list
    for yy in list:
        #print(yy)

        #print(os.path.isdir(str(gl_str[0]+'/'+yy)))
        if os.path.isdir(str(gl_str[0]+'/'+yy)):
            recursion_list( yy, gl_str ,dnk_struct,  1 ,res , arrr )



proj_data='/Dog/abc/abc_0040'
out={}
out['iter']=arrr
out_str = json.dumps(out)

#print(out_str)

sheet_in=ggl_get.get_sheets( proj_data)
ggl_sheets=sheet_in['main'].keys()
print (sheet_in['main'].keys())


out_list = [i for i in arrr if i not in ggl_sheets]

print (out_list)
out_list.insert(0, '')


sheet=add_collumns_sheets( proj_data , 'main', 'A' , out_list )

#data=sheet['main'][proj_data]['Y']
#data=sheet['main']
#print (data)














