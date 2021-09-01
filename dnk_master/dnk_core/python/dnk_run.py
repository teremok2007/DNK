import os
import sys
import json
from DNK.dnk_master.dnk_core.python.dnk_utils import dnk_init
import google_sheet_get as ggl_get

dnk_globals = dnk_init.dnk_globals()
os.environ["CGRU_LOCATION"] = dnk_globals["CGRU_LOCATION"]
cgru_libs = dnk_globals["CGRU_LOCATION"] + "/lib/python/"
lib_path = os.path.abspath(cgru_libs)
sys.path.append(lib_path)

cgru_libs = dnk_globals["CGRU_LOCATION"] + "/afanasy/python/"
lib_path = os.path.abspath(cgru_libs)
sys.path.append(lib_path)


import af_dnk_actions as dnk_act

node_in = str(sys.argv[1])
iterator = json.loads(sys.argv[2])

proj_sheets = ggl_get.get_sheets(iterator[0])


for it in iterator:
    dnk_act.runSelectUpStream(it, node_in, proj_sheets)
