module.exports = {

  get_graph_info: function (resp_out , dnk_project_path , navi_dir) {

  	const fs = require('fs')
  	const path = require('path');



    dnk_struct_array=[ 'prj' , 'ctx' ];

  	full_navi_path=dnk_project_path+'/'+ navi_dir
    navi_dir_array=navi_dir.split('/')
    navi_dir_array = navi_dir_array.filter(val => val !== "");

    if (navi_dir_array.length>1) {
        init_path=dnk_project_path+'/'+navi_dir_array[0]+'/_init_';
        if (fs.existsSync(init_path)) {
	        let proj_init = fs.readFileSync(init_path);
	        let init_data = JSON.parse(proj_init);
            dnk_contexts_map=init_data['dnk_contexts_map'][navi_dir_array[1]][0].split('/').filter(val => val !== "");
            dnk_struct_array=dnk_struct_array.concat(dnk_contexts_map);

        }
    }


    cur_dnk_path='';
    all_files_array=[];
    all_files_array_name=[];
    i=0;
    navi_dir_array.forEach(cur_dir => {
        cur_dnk_path=cur_dnk_path+'/'+cur_dir;
        search_dir=dnk_project_path+cur_dnk_path;
        all_files = fs.readdirSync(search_dir , { withFileTypes: true }).filter(d => d.isFile()).map(d => d.name).map(function(a) { return cur_dnk_path +'/'+ a; });
        all_files_names = fs.readdirSync(search_dir , { withFileTypes: true }).filter(d => d.isFile()).map(d => d.name).map(function(a) { return '['+dnk_struct_array[i]+']'; });
        all_files_array=all_files_array.concat(all_files);
        all_files_array_name=all_files_array_name.concat(all_files_names);
        i=i+1;
    });


    dirs = fs.readdirSync(full_navi_path , { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name);
    files = fs.readdirSync(full_navi_path , { withFileTypes: true }).filter(d => d.isFile()).map(d => d.name);

    resp_out["files_arr"]=files;
    resp_out["dir_arr"]=dirs;

    const dbox=[];
    const doit={};
    i=0;
	all_files_array.forEach(file => {
		file_path=dnk_project_path+'/'+file;
		console.log(file_path);
        refix_file=all_files_array_name[i]
		if (path.extname(file) == ".doit"){
			
			let rawdata = fs.readFileSync(file_path);
			let doit_data = JSON.parse(rawdata);
			//doit[path.parse(file).name]=doit_data;
			doit[(refix_file+path.parse(file).name)]=doit_data;
			console.log(path.parse(file).name)
		}

		if (path.extname(file) == ".dbox"){
			dbox.push(path.parse(file).name);
			}
		i=i+1;
	})

	resp_out["doit_arr"]=doit;
	resp_out["dbox_arr"]=dbox;


    return resp_out;
  },


  no_work: function () {
  // whatever
  }

};





var zemba = function () {
}