from .dnk_path import DnkPath as dp

# from dnk_path import DnkPath as dp
import os
import re

out_array = set()

def file_to_json(json_path):
    import json
    with open(json_path) as f:
        init_proj_dict = json.load(f)
    return init_proj_dict


def get_context_expression_variable_name(expression_str):
    rl = re.compile(r"{{[^}}]+}}")
    find_expressions = re.findall(rl, expression_str)  # find {{body}}

    if find_expressions == []:
        return None
    variable_name = ""
    for it_expr in find_expressions:

        res = (
            str(it_expr)
            .replace(" ", "")
            .replace("{{", "")
            .replace("}}", "")
            .replace("[", "")
            .replace("]", "")
        )
        try:
            variable_name = res.split("=")[0]
        except:
            return None

    return variable_name


# => {{ work=[*, anima ,render] }} => Array[ *, anima, render ]
def solve_context_expression(path_for_search, expression_str):

    rl = re.compile(r"{{[^}}]+}}")
    find_expressions = re.findall(rl, expression_str)  # find {{body}}

    if find_expressions == []:
        return {expression_str}

    out_item = set()

    for it_expr in find_expressions:

        res = (
            str(it_expr)
            .replace(" ", "")
            .replace("{{", "")
            .replace("}}", "")
            .replace("[", "")
            .replace("]", "")
        )

        try:
            expression_body_array = res.split("=")[1].split(",")
        except:
            return {res}

        for it_body in expression_body_array:
            if it_body == "*":
                try:
                    out_item = out_item.union(set(os.listdir(path_for_search)))
                except:
                    return None
                continue
            if "^" in it_body:
                out_item.discard(it_body.replace("^", ""))
                continue
            if it_body != "":
                out_item.add(it_body)

    return out_item


def context_parser_recursive(
    current_folder, context_array, deep, path_for_search
):

    if not os.path.exists(path_for_search.to_str()):
        return 1
    deep_update = deep + 1

    path_for_search_update = path_for_search.join(current_folder)
    try:
        expression_str = context_array[deep_update]
    except:
        out_array.add(path_for_search_update.to_str())
        return 1

    folder_search_array = solve_context_expression(
        path_for_search_update.to_str(), expression_str
    )
    if folder_search_array == None:
        return 1

    for folder in folder_search_array:
        context_parser_recursive(
            current_folder=folder,
            context_array=context_array,
            deep=deep_update,
            path_for_search=path_for_search_update,
        )
    return 1


def context_parser_start(studio_proj, current_context_body):
    path_for_search = dp(studio_proj)
    context_array = current_context_body.split("/")


    path_for_search = path_for_search.join(context_array[0])
    expression_str = context_array[1]

    folder_search_array = solve_context_expression(
        path_for_search.to_str(), expression_str
    )

    for folder in folder_search_array:
        context_parser_recursive(
            current_folder=folder,
            context_array=context_array,
            deep=1,
            path_for_search=path_for_search,
        )

    return list(out_array)


def context_to_dnk_map(
    studio_proj,
    current_proj_name,
    current_context_body,
    current_context_name,
    dnk_contexts_map,
):
    array_dirs = context_parser_start(studio_proj, current_context_body)

    context_array = str(current_context_body).split("/")
    dnk_contexts_map_array = str(dnk_contexts_map[0]).split("/")
    dnk_contexts_map_array_clean = [
        i for i in dnk_contexts_map_array if i != ""
    ]

    context_array_clear = [i for i in context_array if i != ""]
    dnk_struct_iter_array = []
    for iter_dir in array_dirs:
        out_dict = {}
        separate_path_array = str(iter_dir).replace(studio_proj, "").split("/")
        separate_path_clear = [i for i in separate_path_array if i != ""]

        for t in zip(context_array_clear, separate_path_clear):
            if get_context_expression_variable_name(t[0]) != None:
                out_dict[get_context_expression_variable_name(t[0])] = t[1]

        dnk_path = dp("").join(current_proj_name).join(current_context_name)
        for dnk_map_iter in dnk_contexts_map_array_clean:
            dnk_path = dnk_path.join(out_dict[dnk_map_iter])
        dnk_struct_iter_array.append(dnk_path.to_str())

    out_dnk_struct_iter_array = list(set(dnk_struct_iter_array))

    return out_dnk_struct_iter_array


def get_contexts_from_path(path, proj, dnk_globals):

    dnk_proj_root = dp(dnk_globals["dnk_proj_root"])
    dnk_proj_ini = dnk_proj_root.join(proj).join('_init_')
    if os.path.exists(dnk_proj_ini.to_str()):
        try:
            init_dict = file_to_json(dnk_proj_ini.to_str())
        except:
            return {}
    else:
        return {}

    out_dict = {}

    contexts = init_dict['contexts']

    path_array=path.split('/')
    for cont_it in list(contexts.keys()):
        out_dict = {}
        current_context_body = str('/'+contexts[cont_it]+'/').replace('//', '/')
        print([path, current_context_body])
        i = 0
        out_cont={}
        for it in current_context_body.split('/'):
            vary_name = get_context_expression_variable_name(it)
            path_item = path_array[i]

            if path_item == '' or it == '':
                i = i+1
                continue

            if vary_name is None and it != path_item:
                out_cont = {}
                out_dict = {}
                break
            elif vary_name is None and it == path_item:
                i = i+1
                continue
            else:
                print([it, vary_name, path_item])
                out_cont[vary_name] = path_item
            i = i+1

        if out_cont != {}:
            out_dict[cont_it] = out_cont
            break

    return out_dict