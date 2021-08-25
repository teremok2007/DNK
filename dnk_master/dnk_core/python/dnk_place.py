import json
from dnk_utils import dnk_init

from dnk_utils import dnk_path as dp
from dnk_utils import dnk_context as ctx

def create_dnk_context(current_proj, context_name):

    dnk_globals = dnk_init.dnk_globals()
    studio_proj = dp.DnkPath(dnk_globals['studio_proj']).join(current_proj)

    proj_root_path = dp.DnkPath(dnk_globals['dnk_proj_root'])

    dnk_proj_path = proj_root_path.join(current_proj)
    dnk_proj_init = proj_root_path.join(current_proj).join('_init_')


    init_proj_dict = {}
    with open(dnk_proj_init.to_str()) as f:
        init_proj_dict = json.load(f)

    current_context = init_proj_dict['contexts'][context_name]
    res = ctx.context_parser_start(studio_proj.to_str(), current_context)
    return res

print(create_dnk_context( 'Cat' , 'shots' ))
