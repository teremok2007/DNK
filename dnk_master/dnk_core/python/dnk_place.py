import json
from dnk_utils import dnk_init

from dnk_utils import dnk_path as dp
from dnk_utils import dnk_context as ctx


def iterator_from_context(current_proj, context_name):

    dnk_globals = dnk_init.dnk_globals()
    studio_proj = dp.DnkPath(dnk_globals["studio_proj_root"]).join(
        current_proj
    )
    proj_root_path = dp.DnkPath(dnk_globals["dnk_proj_root"])

    dnk_proj_path = proj_root_path.join(current_proj)
    dnk_proj_init = proj_root_path.join(current_proj).join("_init_")

    dnk_run_projects = dnk_globals["run_projects"]
    if current_proj not in dnk_run_projects:
        return []


    init_proj_dict = {}
    with open(dnk_proj_init.to_str()) as f:
        init_proj_dict = json.load(f)
    if context_name in init_proj_dict["contexts"]:
        current_context = init_proj_dict["dnk_contexts_map"][context_name]
        dnk_contexts_map = init_proj_dict["dnk_contexts_map"][context_name]
    else:
        return ['Context_name_ERROR']

    try:
        res = ctx.context_parser_start(studio_proj.to_str(), current_context)
    except:
        return ['Get_context_array_ERROR']

    try:
        dnk_iterator = ctx.context_to_dnk_map(
            studio_proj.to_str(),
            current_proj,
            current_context,
            context_name,
            dnk_contexts_map,
        )
    except:
        return ['Create_context_from_map_ERROR']

    return dnk_iterator


def context_from_path(path_string):

    dnk_globals = dnk_init.dnk_globals()
    studio_proj = dp.DnkPath(dnk_globals["studio_proj_root"])
    actual_path = path_string.split(studio_proj.to_str())[1]

    proj = actual_path.split('/')[0]
    context_path = str('/'+actual_path.split(proj)[1]+'/').replace('//', '/')
    contexts = ctx.get_contexts_from_path(context_path, proj, dnk_globals)
    return contexts



