import sys
import json
import os
from pathlib import Path

dnk_location_in = str(Path(os.path.realpath(__file__)).parents[4])
dnk_python = str(dnk_location_in + "/dnk_master/dnk_core/python/").replace(
    "\\", "/"
)
sys.path.append(dnk_python)

import dnk_place


project = str(sys.argv[1])
context = str(sys.argv[2])

array = dnk_place.iterator_from_context(project, context)

out = {}
out["iter"] = array
out_str = json.dumps(out)

print(out_str)
