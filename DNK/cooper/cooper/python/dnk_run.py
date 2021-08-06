
import os
import sys
import json
import google_sheet_get as ggl_get


os.environ["CGRU_LOCATION"] = "R:/06_Tools/Revo/cgru.3.2.0.windows/cgru.3.2.0/"
dnk_libs ='R:/06_Tools/Revo/cgru.3.2.0.windows/cgru.3.2.0/lib/python/'
lib_path = os.path.abspath(dnk_libs)
sys.path.append(lib_path)


dnk_libs ='R:/06_Tools/Revo/cgru.3.2.0.windows/cgru.3.2.0/afanasy/python/'
lib_path = os.path.abspath(dnk_libs)
sys.path.append(lib_path)




import af_dnk_actions as dnk_act

node_in=str(sys.argv[1])
iterator=json.loads(sys.argv[2])

proj_sheets=ggl_get.get_sheets(iterator[0])

#with open('R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper_tmp/data.json', 'w') as f:
    #json.dump(proj_sheets, f , indent=4)

#proj_sheets={}

for it in iterator:
	dnk_act.runSelectUpStream( it , node_in , proj_sheets )

