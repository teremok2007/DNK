import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from DNK.dnk_master.dnk_core.python.dnk_utils import dnk_init as cu_init
import cooper_monitors as cu_moni
import string






def createAlphabetDict(iter):
    off=0
    d={}
    ch=[]
    for i in range(1,iter):
        for n, ch in (enumerate(string.ascii_uppercase)):        
            d[n+off]=ch*i
        off=off+26  
    return d






def get_sheets( proj_data ):

    proj=proj_data.split('/')[1]

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




    results = service.spreadsheets().get(spreadsheetId = spreadsheetId, includeGridData = True).execute()

    out_sh_dict={}

    for sh in results['sheets']:
        sh_data={}
        coll_arr=[]
        list_name=sh['properties']['title']
        if 'rowData' in list(sh['data'][0].keys()):
            coll_arr=sh['data'][0]['rowData']
        coll_dict={}
        a=0
        for i in coll_arr:

            #print(list(i['values'][0].keys()))
            if 'formattedValue' in list(i['values'][0].keys()):

                row_dict={}
                row_dict['id']=a+1
                c=0
                for rw in i['values']:
                    if 'formattedValue' in list(rw.keys()):
                        row_dict[alpha[c]] = rw['formattedValue']
                        c=c+1
                    else:
                        row_dict[alpha[c]]='_dnk_no_row_'
                        c=c+1


                coll_dict[i['values'][0]['formattedValue']]=row_dict


            else:
                a=a+1
                continue

            a=a+1
        out_sh_dict[list_name]=coll_dict



    ##################### _list_###################__v__########__h__##############
    #result_from_google_sheet=results['sheets'][0]['data'][0]['rowData'][0]['values'][1]['formattedValue']


    return out_sh_dict


######_EXAMPLE_####################












