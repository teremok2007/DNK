







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

        fs.writeFileSync(dnk_sheet_path, JSON.stringify(out_sheet_dict, null, 4));

    return dnk_sheet_path;

    }










}





var zemba = function () {

}