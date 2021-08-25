# from .dnk_path import DnkPath as dp
from dnk_path import DnkPath as dp
import os
import re


# => {{ work=[*, anima ,render] }} => Array[ *, anima, render ]
def solve_context_expression(path_for_search, expression_str):
    rl = re.compile(r'{{[^}}]+}}')
    find_expressions = re.findall(rl, expression_str)  # find {{body}}

    if find_expressions == []:
        return {expression_str}

    out_item = set()

    for it_expr in find_expressions:

        res = str(it_expr).replace(' ', '').replace('{{', '').replace('}}', '').replace('[', '').replace(']', '')

        try:
            expression_body_array = res.split('=')[1].split(',')
        except:
            return {res}

        for it_body in expression_body_array:
            if it_body == '*':
                out_item = out_item.union(set(os.listdir(path_for_search)))
                continue

            if "^" in it_body:
                out_item.discard(it_body.replace('^', ''))
                continue
            if it_body != '':
                out_item.add(it_body)

    return out_item


def context_parser_recursive(current_folder, context_array, deep, path_for_search):
    deep_update = deep+1
    #print(current_folder)
    path_for_search_update = path_for_search.join(current_folder)
    try:
        expression_str = context_array[deep_update]
    except:
        print (path_for_search_update.to_str())
        return 1
    folder_search_array = solve_context_expression(path_for_search_update.to_str(), expression_str)
    #print(folder_search_array)
    for folder in folder_search_array:
        context_parser_recursive(current_folder=folder, context_array=context_array, deep=deep_update,
                                 path_for_search=path_for_search_update)
    return 1


def context_parser_start(studio_proj, current_context):
    path_for_search = dp(studio_proj)
    context_array = current_context.split('/')
    #print(context_array)



    path_for_search = path_for_search.join(context_array[0])
    expression_str = context_array[1]

    folder_search_array = solve_context_expression(path_for_search.to_str(), expression_str)

    for folder in folder_search_array:
        context_parser_recursive(current_folder=folder, context_array=context_array, deep=1, path_for_search=path_for_search)



    return folder_search_array


context_parser_start('C:/proj/Cat/',
                           "/{{ work=[anima,render] }}/{{ seq=[*] }}/shots/{{ shot=[*]> }}/steps/{{ step=[p0] }}/tasks/{{ task=[p1] }}/")
