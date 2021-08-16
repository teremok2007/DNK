import os
import json
from pathlib import Path

def dnk_proxy():
	return 1



def dnk_globals():

	dnk_location_in = str( Path(__file__).parents[3] )
	dnk_location=dnk_location_in.replace('\\' , '/')

	dnk_init_file = os.path.join(dnk_location, 'dnk_init.json')
	print(dnk_init_file)

	init = {}
	with open(dnk_init_file) as f:
		init = json.load(f)

	init["dnk_proj"] = dnk_location + "/dnk_master/dnk_proj/"
	init["dnk_user"] = dnk_location + "/dnk_master/dnk_users/"
	init["dnk_python"] = dnk_location + "/dnk_master/dnk_core/python/"
	init["dnk_scripts"] = dnk_location + "/dnk_master/dnk_core/scripts/"

	return init

a=dnk_globals()
print(a)