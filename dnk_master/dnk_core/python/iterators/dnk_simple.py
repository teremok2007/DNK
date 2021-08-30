
import sys
sys.path.append('R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/python')

import cooper_init as cu_init
import cooper_monitors as cu_moni
import json
import os







def recursion_list( y , gl_str ,dnk_struct , depth , res , arr ):
	res=res+'/'+y
	if depth==(len(dnk_struct)-1):
		#print('ASD')
		res_out='/'+res
		arr.append(res_out)
		return 1

	smask=gl_str[0]+'/'+str(y)+'/'+gl_str[1]
	#print(smask)
	depth=depth+1

	xx=dnk_struct[depth]
	gl_strr=smask.split(str('{{'+xx+'}}'))

	list=os.listdir(gl_strr[0])

	for yyy in list:
		if yyy[0]=='_':
			continue

		#print(os.path.isdir(str(gl_strr[0]+'/'+yyy)))
		if os.path.isdir(str(gl_strr[0]+'/'+yyy)):
			recursion_list( yyy, gl_strr ,dnk_struct, depth , res, arr )




init=cu_init.Cooper_Globals()



cu_proj    = init['cooper_proj']
studio_proj= init['studio_proj']
run_proj   = init['run_projects']

arrr=[]
for i in run_proj:
    my_proj=cu_moni.get_proj_data(i)
    dnk_struct=my_proj['dnk_project_structure']
    mask=str(my_proj['group_mask'][0])
    maask=mask.replace(str('{{'+dnk_struct[0]+'}}'), i)
    aa=dnk_struct[1]
    gl_str=maask.split(str('{{'+aa+'}}'))
    res=i
    list=os.listdir(gl_str[0])
    #print list
    for yy in list:
        #print(yy)
        #print(os.path.isdir(str(gl_str[0]+'/'+yy)))
        if os.path.isdir(str(gl_str[0]+'/'+yy)):
            recursion_list( yy, gl_str ,dnk_struct,  1 ,res , arrr )




out={}
out['iter']=arrr
out_str = json.dumps(out)

#with open('R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper_tmp/data.json', "w") as write_file:
#	json.dump(out_str, write_file, indent=4)
#out_str="{\"iter\": [\"Dog/abc/abc_0010\", \"Dog/abc/abc_0020\", \"Dog/abc/abc_0030\", \"Dog/abc/abc_0040\", \"Dog/abc/abc_0050\", \"Dog/abc/abc_0060\", \"Dog/abc/abc_0070\", \"Dog/adk/adk_0010\", \"Dog/adk/adk_0020\", \"Dog/adk/adk_0030\", \"Dog/adk/adk_0040\", \"Dog/adk/adk_0050\", \"Dog/aop/aop_0010\", \"Dog/aop/aop_0020\", \"Dog/aop/aop_0030\", \"Dog/aop/aop_0040\", \"Dog/aop/aop_0050\", \"Dog/aph/aph_0010\", \"Dog/aph/aph_0020\", \"Dog/aph/aph_0030\", \"Dog/aph/aph_0040\", \"Dog/aph/aph_0050\", \"Dog/aph/aph_0060\", \"Dog/aph/aph_0070\", \"Dog/aph/aph_0080\", \"Dog/aph/aph_0090\", \"Dog/aph/aph_0100\", \"Dog/aph/aph_0110\", \"Dog/aph/aph_0120\", \"Dog/aph/aph_0130\", \"Dog/aph/aph_0140\", \"Dog/aph/aph_0150\", \"Dog/aph/aph_0160\", \"Dog/aph/aph_0170\", \"Dog/aph/aph_0171\", \"Dog/aph/aph_0180\", \"Dog/aph/aph_0190\", \"Dog/aph/aph_0200\", \"Dog/aph/aph_0210\", \"Dog/aph/aph_0220\", \"Dog/aph/aph_0230\", \"Dog/aph/aph_0240\", \"Dog/aph/aph_0250\", \"Dog/aph/aph_0260\", \"Dog/aph/aph_0270\", \"Dog/aph/aph_0280\", \"Dog/aph/aph_0290\", \"Dog/aph/aph_0300\", \"Dog/aph/aph_0310\", \"Dog/aph/aph_0320\", \"Dog/aph/aph_0330\", \"Dog/aph/aph_0340\", \"Dog/aph/aph_0350\", \"Dog/aph/aph_0360\", \"Dog/aph/aph_0370\", \"Dog/aph/aph_0380\", \"Dog/bfc/bfc_0010\", \"Dog/bfc/bfc_0020\", \"Dog/bfc/bfc_0030\", \"Dog/bfc/bfc_0040\", \"Dog/bfc/bfc_0060\", \"Dog/bfc/bfc_0070\", \"Dog/bfc/bfc_0080\", \"Dog/bfc/bfc_0090\", \"Dog/bfc/bfc_0100\", \"Dog/bfc/bfc_0110\", \"Dog/bic/bic_0010\", \"Dog/bic/bic_0020\", \"Dog/bic/bic_0030\", \"Dog/bic/bic_0040\", \"Dog/bic/bic_0050\", \"Dog/bic/bic_0060\", \"Dog/bic/bic_0070\", \"Dog/bic/bic_0080\", \"Dog/bic/bic_0090\", \"Dog/bic/bic_0100\", \"Dog/bic/bic_0110\", \"Dog/bic/bic_0120\", \"Dog/bic/bic_0130\", \"Dog/bic/bic_0140\", \"Dog/bic/bic_0150\", \"Dog/bic/bic_0160\", \"Dog/bic/bic_0170\", \"Dog/bic/bic_0180\", \"Dog/bic/bic_0190\", \"Dog/bic/bic_0200\", \"Dog/bic/bic_0210\", \"Dog/bic/bic_0220\", \"Dog/bic/bic_0230\", \"Dog/bic/bic_0240\", \"Dog/bic/bic_0250\", \"Dog/bic/bic_0260\", \"Dog/bic/bic_0270\", \"Dog/bic/bic_0280\", \"Dog/bic/bic_0290\", \"Dog/bnh/bnh_0010\", \"Dog/brt/brt_0010\", \"Dog/brt/brt_0020\", \"Dog/brt/brt_0030\", \"Dog/brt/brt_0040\", \"Dog/brt/brt_0050\", \"Dog/brt/brt_0060\", \"Dog/brt/brt_0070\", \"Dog/brt/brt_0080\", \"Dog/brt/brt_0090\", \"Dog/brt/brt_0100\", \"Dog/brt/brt_0110\", \"Dog/brt/brt_0130\", \"Dog/brt/brt_0140\", \"Dog/brt/brt_0150\", \"Dog/btp/btp_0010\", \"Dog/btp/btp_0020\", \"Dog/btp/btp_0030\", \"Dog/btp/btp_0040\", \"Dog/btp/btp_0050\", \"Dog/btp/btp_0060\", \"Dog/btp/btp_0070\", \"Dog/btp/btp_0080\", \"Dog/btp/btp_0090\", \"Dog/btp/btp_0100\", \"Dog/btp/btp_0110\", \"Dog/btp/btp_0120\", \"Dog/btp/btp_0130\", \"Dog/btp/btp_0140\", \"Dog/btp/btp_0150\", \"Dog/btp/btp_0160\", \"Dog/btp/btp_0170\", \"Dog/btp/btp_0180\", \"Dog/btp/btp_0190\", \"Dog/btp/btp_0200\", \"Dog/btp/btp_0210\", \"Dog/btp/btp_0220\", \"Dog/cdh/cdh_0010\", \"Dog/cdh/cdh_0020\", \"Dog/cdh/cdh_0030\", \"Dog/cdh/cdh_0040\", \"Dog/cdh/cdh_0050\", \"Dog/cdh/cdh_0060\", \"Dog/cdh/cdh_0070\", \"Dog/cdh/cdh_0080\", \"Dog/cdh/cdh_0090\", \"Dog/cdh/cdh_0100\", \"Dog/cdh/cdh_0110\", \"Dog/dbf/dbf_0010\", \"Dog/dbf/dbf_0020\", \"Dog/dbf/dbf_0030\", \"Dog/dbf/dbf_0040\", \"Dog/dbf/dbf_0050\", \"Dog/dbh/dbh_0010\", \"Dog/dbh/dbh_0020\", \"Dog/dbh/dbh_0030\", \"Dog/dbn/dbn_0010\", \"Dog/dbn/dbn_0020\", \"Dog/dbn/dbn_0030\", \"Dog/dbn/dbn_0040\", \"Dog/dbn/dbn_0050\", \"Dog/dbn/dbn_0060\", \"Dog/dbn/dbn_0070\", \"Dog/dbn/dbn_0080\", \"Dog/dbn/dbn_0090\", \"Dog/dbn/dbn_0100\", \"Dog/dcc/dcc_0010\", \"Dog/dcc/dcc_0020\", \"Dog/dcc/dcc_0030\", \"Dog/dci/dci_0010\", \"Dog/dci/dci_0020\", \"Dog/dci/dci_0030\", \"Dog/dci/dci_0040\", \"Dog/dci/dci_0050\", \"Dog/dci/dci_0060\", \"Dog/dci/dci_0070\", \"Dog/dci/dci_0080\", \"Dog/dci/dci_0090\", \"Dog/dci/dci_0100\", \"Dog/dec/dec_0010\", \"Dog/dec/dec_0020\", \"Dog/dec/dec_0030\", \"Dog/dfr/dfr_0010\", \"Dog/dfr/dfr_0020\", \"Dog/dfr/dfr_0040\", \"Dog/dfr/dfr_0050\", \"Dog/dfr/dfr_0060\", \"Dog/dfr/dfr_0070\", \"Dog/dfr/dfr_0075\", \"Dog/dfr/dfr_0080\", \"Dog/dfr/dfr_0090\", \"Dog/dfr/dfr_0100\", \"Dog/dfr/dfr_0110\", \"Dog/dfr/dfr_0120\", \"Dog/dfr/dfr_0130\", \"Dog/dfr/dfr_0140\", \"Dog/dfr/dfr_0150\", \"Dog/dfr/dfr_0160\", \"Dog/dfr/dfr_0170\", \"Dog/dfr/dfr_0180\", \"Dog/dfr/dfr_0190\", \"Dog/dfr/dfr_0210\", \"Dog/dfr/dfr_0220\", \"Dog/dfr/dfr_0240\", \"Dog/dhr/dhr_0010\", \"Dog/dhr/dhr_0030\", \"Dog/dhr/dhr_0040\", \"Dog/dhr/dhr_0060\", \"Dog/dhr/dhr_0070\", \"Dog/dhr/dhr_0080\", \"Dog/dhr/dhr_0090\", \"Dog/dhr/dhr_0100\", \"Dog/dhr/dhr_0110\", \"Dog/dhr/dhr_0120\", \"Dog/dhr/dhr_0130\", \"Dog/dhr/dhr_0140\", \"Dog/dhr/dhr_0150\", \"Dog/dhr/dhr_0160\", \"Dog/dhr/dhr_0170\", \"Dog/dhr/dhr_0180\", \"Dog/dhr/dhr_0190\", \"Dog/dhr/dhr_0220\", \"Dog/dhr/dhr_0240\", \"Dog/dhr/dhr_0250\", \"Dog/dhr/dhr_0260\", \"Dog/dhr/dhr_0270\", \"Dog/dhr/dhr_0280\", \"Dog/dhr/dhr_0290\", \"Dog/dhr/dhr_0300\", \"Dog/dhr/dhr_0305\", \"Dog/dhr/dhr_0310\", \"Dog/dhr/dhr_0320\", \"Dog/dhr/dhr_0330\", \"Dog/dhr/dhr_0340\", \"Dog/dhr/dhr_0350\", \"Dog/dhr/dhr_0360\", \"Dog/dhr/dhr_0370\", \"Dog/dhr/dhr_0380\", \"Dog/dhr/dhr_0390\", \"Dog/dhr/dhr_0400\", \"Dog/dhr/dhr_0410\", \"Dog/dmf/dmf_0010\", \"Dog/dmf/dmf_0030\", \"Dog/dmf/dmf_0040\", \"Dog/dmf/dmf_0050\", \"Dog/dmw/dmw_0010\", \"Dog/dmw/dmw_0020\", \"Dog/dmw/dmw_0030\", \"Dog/dmw/dmw_0040\", \"Dog/dmw/dmw_0050\", \"Dog/dmw/dmw_0060\", \"Dog/dmw/dmw_0070\", \"Dog/dmw/dmw_0072\", \"Dog/dmw/dmw_0074\", \"Dog/dmw/dmw_0076\", \"Dog/dmw/dmw_0080\", \"Dog/dmw/dmw_0090\", \"Dog/dmw/dmw_0110\", \"Dog/dmw/dmw_0120\", \"Dog/dph/dph_0010\", \"Dog/dph/dph_0020\", \"Dog/dph/dph_0030\", \"Dog/dph/dph_0040\", \"Dog/dph/dph_0050\", \"Dog/dph/dph_0060\", \"Dog/dph/dph_0070\", \"Dog/dph/dph_0080\", \"Dog/dph/dph_0090\", \"Dog/dph/dph_0100\", \"Dog/dph/dph_0110\", \"Dog/dph/dph_0120\", \"Dog/dph/dph_0130\", \"Dog/dph/dph_0140\", \"Dog/dph/dph_0150\", \"Dog/dsq/dsq_0010\", \"Dog/dsq/dsq_0020\", \"Dog/dsq/dsq_0030\", \"Dog/dsq/dsq_0040\", \"Dog/dsq/dsq_0050\", \"Dog/dsq/dsq_0060\", \"Dog/dsq/dsq_0070\", \"Dog/dwa/dwa_0010\", \"Dog/dwa/dwa_0020\", \"Dog/dwa/dwa_0030\", \"Dog/dwa/dwa_0060\", \"Dog/dwa/dwa_0070\", \"Dog/dwa/dwa_0080\", \"Dog/dwa/dwa_0090\", \"Dog/dwa/dwa_0100\", \"Dog/dwa/dwa_0110\", \"Dog/dwa/dwa_0120\", \"Dog/dwa/dwa_0130\", \"Dog/dwa/dwa_0140\", \"Dog/dwa/dwa_0150\", \"Dog/dwa/dwa_0160\", \"Dog/dwa/dwa_0170\", \"Dog/dwa/dwa_0180\", \"Dog/fnc/fnc_0010\", \"Dog/fnc/fnc_0020\", \"Dog/fnc/fnc_0030\", \"Dog/fnc/fnc_0040\", \"Dog/fnc/fnc_0050\", \"Dog/fnc/fnc_0060\", \"Dog/fnc/fnc_0070\", \"Dog/fnc/fnc_0080\", \"Dog/fnc/fnc_0090\", \"Dog/gfc/gfc_0010\", \"Dog/gfc/gfc_0020\", \"Dog/gfc/gfc_0030\", \"Dog/gfo/gfo_0010\", \"Dog/gfo/gfo_0020\", \"Dog/gfo/gfo_0030\", \"Dog/gfo/gfo_0040\", \"Dog/gfo/gfo_0050\", \"Dog/gfo/gfo_0060\", \"Dog/gfo/gfo_0070\", \"Dog/gfo/gfo_0080\", \"Dog/gfo/gfo_0090\", \"Dog/gfo/gfo_0100\", \"Dog/gfo/gfo_0110\", \"Dog/gfo/gfo_0120\", \"Dog/gfo/gfo_0130\", \"Dog/gfo/gfo_0140\", \"Dog/gfo/gfo_0150\", \"Dog/gfo/gfo_0160\", \"Dog/gfo/gfo_0161\", \"Dog/gfo/gfo_0170\", \"Dog/gfo/gfo_0180\", \"Dog/gfo/gfo_0190\", \"Dog/gfo/gfo_0200\", \"Dog/gfo/gf\\u043e_0145\", \"Dog/hcd/hcd_0010\", \"Dog/hcd/hcd_0020\", \"Dog/htd/htd_0010\", \"Dog/htd/htd_0020\", \"Dog/htd/htd_0030\", \"Dog/htd/htd_0040\", \"Dog/htd/htd_0050\", \"Dog/htd/htd_0060\", \"Dog/htd/htd_0070\", \"Dog/htd/htd_0080\", \"Dog/htd/htd_0090\", \"Dog/hwt/hwt_0010\", \"Dog/hwt/hwt_0020\", \"Dog/hwt/hwt_0030\", \"Dog/hwt/hwt_0034\", \"Dog/hwt/hwt_0035\", \"Dog/hwt/hwt_0040\", \"Dog/hwt/hwt_0050\", \"Dog/hwt/hwt_0060\", \"Dog/hwt/hwt_0070\", \"Dog/hwt/hwt_0080\", \"Dog/hwt/hwt_0090\", \"Dog/hwt/hwt_0100\", \"Dog/lsb/lsb_0010\", \"Dog/lsb/lsb_0020\", \"Dog/lsb/lsb_0030\", \"Dog/lsb/lsb_0040\", \"Dog/lsb/lsb_0050\", \"Dog/lsb/lsb_0060\", \"Dog/lsb/lsb_0070\", \"Dog/lsb/lsb_0080\", \"Dog/lsb/lsb_0090\", \"Dog/lsb/lsb_0100\", \"Dog/lsb/lsb_0110\", \"Dog/lsb/lsb_0120\", \"Dog/lsb/lsb_0130\", \"Dog/lsb/lsb_0140\", \"Dog/ohp/ohp_0010\", \"Dog/ohp/ohp_0040\", \"Dog/ohp/ohp_0050\", \"Dog/ohp/ohp_0070\", \"Dog/ohp/ohp_0080\", \"Dog/ohp/ohp_0090\", \"Dog/ohp/ohp_0100\", \"Dog/ohp/ohp_0110\", \"Dog/ohp/ohp_0120\", \"Dog/ohp/ohp_0130\", \"Dog/ohp/ohp_0140\", \"Dog/ohp/ohp_0150\", \"Dog/ohp/ohp_0160\", \"Dog/ohp/ohp_0170\", \"Dog/ohp/ohp_0180\", \"Dog/ohp/ohp_0190\", \"Dog/ohp/ohp_0200\", \"Dog/ohp/ohp_0210\", \"Dog/ohp/ohp_0220\", \"Dog/ohp/ohp_0230\", \"Dog/ohp/ohp_0240\", \"Dog/ohp/ohp_0250\", \"Dog/ohp/ohp_0260\", \"Dog/ppm/ppm_0020\", \"Dog/ppm/ppm_0030\", \"Dog/ppm/ppm_0040\", \"Dog/ppm/ppm_0050\", \"Dog/ppm/ppm_0060\", \"Dog/ppm/ppm_0070\", \"Dog/ppm/ppm_0080\", \"Dog/ppm/ppm_0090\", \"Dog/ppm/ppm_0100\", \"Dog/ppm/ppm_0110\", \"Dog/ppm/ppm_0120\", \"Dog/ppm/ppm_0130\", \"Dog/ppm/ppm_0133\", \"Dog/ppm/ppm_0136\", \"Dog/ppm/ppm_0140\", \"Dog/ppm/ppm_0150\", \"Dog/ppm/ppm_0160\", \"Dog/ppm/ppm_0170\", \"Dog/ppm/ppm_0180\", \"Dog/ppm/ppm_0190\", \"Dog/ppm/ppm_0200\", \"Dog/ppm/ppm_0210\", \"Dog/prf/prf_0010\", \"Dog/prf/prf_0020\", \"Dog/prf/prf_0030\", \"Dog/prf/prf_0040\", \"Dog/prf/prf_0050\", \"Dog/prf/prf_0060\", \"Dog/prf/prf_0070\", \"Dog/pwd/pwd_0010\", \"Dog/pwd/pwd_0020\", \"Dog/pwd/pwd_0030\", \"Dog/pwd/pwd_0040\", \"Dog/pwd/pwd_0050\", \"Dog/pwd/pwd_0060\", \"Dog/pwd/pwd_0070\", \"Dog/pwd/pwd_0080\", \"Dog/pwd/pwd_0090\", \"Dog/pwd/pwd_0100\", \"Dog/pwd/pwd_0110\", \"Dog/sfd/sfd_0010\", \"Dog/sfd/sfd_0020\", \"Dog/sfd/sfd_0030\", \"Dog/sfd/sfd_0040\", \"Dog/sfd/sfd_0050\", \"Dog/sfd/sfd_0060\", \"Dog/sfd/sfd_0070\", \"Dog/sfd/sfd_0080\", \"Dog/swt/swt_0010\", \"Dog/swt/swt_0020\", \"Dog/swt/swt_0030\", \"Dog/swt/swt_0040\", \"Dog/swt/swt_0050\", \"Dog/swt/swt_0060\", \"Dog/swt/swt_0070\", \"Dog/swt/swt_0080\", \"Dog/swt/swt_0090\", \"Dog/swt/swt_0100\", \"Dog/swt/swt_0110\", \"Dog/swt/swt_0120\", \"Dog/swt/swt_0130\", \"Dog/swt/swt_0140\", \"Dog/tgi/tgi_0010\", \"Dog/tgi/tgi_0020\", \"Dog/tgi/tgi_0030\", \"Dog/tgi/tgi_0040\", \"Dog/tgi/tgi_0050\", \"Dog/tgi/tgi_0060\", \"Dog/tgi/tgi_0070\", \"Dog/tgi/tgi_0080\"]}"
print(out_str)