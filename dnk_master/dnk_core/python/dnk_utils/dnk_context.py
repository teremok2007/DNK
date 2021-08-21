import re
import dnk_path as dp


def context_parser(context):


    context_array=context.split('/')

    for ctx_it in context:

        res_string = dp.DnkPath('').join(ctx_it)

        rl = re.compile(r'{{[^}}]+}}')
        pr = re.findall(rl, ctx_it)
        print(pr)
        '''
        for ipr in pr:
            ipr_repl=str(ipr).replace(' ', '').replace('{{', '').replace('}}', '')
            a.append(ipr_repl)
        '''
    return a