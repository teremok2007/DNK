







module.exports = {


    add_sheet: function (sheet_info, dnk_proj_path) {
        const fs = require('fs');
        const path = require('path');
        var glob = require('glob');
        out_sheet_dict={};

        sheet_name=sheet_info.sheet_name;
        sheet_get_item=sheet_info.sheet_ctx_type;
        moni_name=sheet_info.moni_name;
        dnk_sheet_path=dnk_proj_path+'/'+moni_name+'/'+sheet_name+'.sheet';

        out_sheet_dict['sheet_get_items']=sheet_get_item;
        out_sheet_dict['height']= 13 ;
        out_sheet_dict['items']=[] ;
        out_sheet_dict['collumns']={};

        collumns_dict={};
        main_collumn_dict={};
        main_collumn_dict['label']='Context';
        main_collumn_dict['width']=25;
        main_collumn_dict['set_data']='none';
        main_collumn_dict['default']= 'none';
        collumns_dict['context']=main_collumn_dict
        out_sheet_dict['collumns']=collumns_dict

        fs.writeFileSync(dnk_sheet_path, JSON.stringify(out_sheet_dict, null, 4));

    return dnk_sheet_path;

    },



    get_sheet: function (in_dict) {
        const fs = require('fs')
        const path = require('path');
        var flatten = require('flat');
        var unflatten = require('flat').unflatten;

        navi_dir = in_dict.ctx;
        sheet_name_ctx = in_dict.sheet_name;
        sheet_name_file=sheet_name_ctx.split(']')[1]
        sheet_ctx_name=sheet_name_ctx.split(']')[0].split('[')[1];
        dnk_project_path = in_dict.dnk_project_path;
        
        let dnk_struct_array=[ 'prj' , 'ctx' ];
        
        full_navi_path=dnk_project_path+'/'+ navi_dir;
        navi_dir_array=navi_dir.split('/');
        navi_dir_array = navi_dir_array.filter(val => val !== "");
        current_depth=navi_dir_array.length-1;


        if (current_depth>0) {
            init_path=dnk_project_path+'/'+navi_dir_array[0]+'/_init_';
            if (fs.existsSync(init_path)) {
                let proj_init = fs.readFileSync(init_path);
                let init_data = JSON.parse(proj_init);
                dnk_contexts_map=init_data['dnk_contexts_map'][navi_dir_array[1]][0].split('/').filter(val => val !== "");
                dnk_struct_array=dnk_struct_array.concat(dnk_contexts_map);

            }
        }



        search_path=dnk_project_path;
        
        for(var i=0; i<navi_dir_array.length;i++){
            search_path=search_path+"/"+navi_dir_array[i];
            search_sheet=search_path+"/"+sheet_name_file;
            var dirfiles = fs.readdirSync(search_path);

            if (dirfiles.indexOf (sheet_name_file) !== -1 && dnk_struct_array[i]==sheet_ctx_name) {
                return  [search_sheet,sheet_ctx_name,dnk_struct_array[i]];
            } 
        }

        




        return in_dict;

    }






}





var zemba = function () {

}