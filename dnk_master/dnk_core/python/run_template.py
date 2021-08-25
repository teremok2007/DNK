import os
import sys
lib_path = os.path.abspath('/studio/abc/users/bocharov/cooper/cooper/python/')
sys.path.append(lib_path)
import subprocess
import json
from DNK.dnk_master.dnk_core.python.dnk_utils import dnk_init

dnk_init.Set_Proxy()

cooper_globals = init.Cooper_Globals()

file='google_sheet_get.py'

#CREDENTIALS_FILE = '/studio/abc/users/bocharov/cooper/cooper_boost/fau-proj-8b665a818604.json'
#list_name='124_render'
#spreadsheetId ='1Z82fRzFT9FcHcYgKqCaNPAlm6nCbmVOad0skzH7zQHI'
#rule_row = "A"
row_name = 'D'
#row_start="2"
#row_end="20"

in_sheets={}
in_sheets['list_name']='124_render'
in_sheets['spreadsheetId']='1Z82fRzFT9FcHcYgKqCaNPAlm6nCbmVOad0skzH7zQHI'
in_sheets['rule_row']='A'
in_sheets['row_start'] = '2'
in_sheets['row_end'] = '20'
in_sheets['CREDENTIALS_FILE']='/studio/abc/users/bocharov/cooper/cooper_boost/fau-proj-8b665a818604.json'

def in_dictionary(key, dict):
    if key in dict:
        return True
    return False




def get_row(row_name , sheets):
    if in_dictionary(row_name,sheets):
        print "It`s Exist"
        return sheets
    else:
        proc=subprocess.Popen(['python3', file , sheets['list_name'] , sheets['spreadsheetId'] ,
        sheets['rule_row'] , row_name , sheets['row_start'] , 
        sheets['row_end'] , sheets['CREDENTIALS_FILE' ] ], 
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        res=proc.stdout.read()

        out = json.loads(res )
        sheets[row_name]=out

        return sheets


my_sheets=get_row(row_name , in_sheets)
print in_sheets[row_name]


def cooper_run_template_down_stream():
   return 1 
