import os
import json
from pathlib import Path

def dnk_proxy():
	return 1



def dnk_globals():

	dnk_location_in = str(Path(__file__).parents[4])
	dnk_location = dnk_location_in.replace('\\', '/')

	dnk_init_file = os.path.join(dnk_location, 'dnk_init.json')


	init = {}
	with open(dnk_init_file) as f:
		init = json.load(f)

	init["dnk_proj_root"] = dnk_location + "/dnk_master/dnk_proj/"
	init["dnk_user"] = dnk_location + "/dnk_master/dnk_users/"
	init["dnk_python"] = dnk_location + "/dnk_master/dnk_core/python/"
	init["dnk_scripts"] = dnk_location + "/dnk_master/dnk_core/scripts/"

	return init

