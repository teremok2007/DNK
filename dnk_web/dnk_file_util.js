







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
        prefix_file=all_files_array_name[i]
		if (path.extname(file) == ".doit"){
			
			let rawdata = fs.readFileSync(file_path);
			let doit_data = JSON.parse(rawdata);
			//doit[path.parse(file).name]=doit_data;
			doit[(prefix_file+path.parse(file).name)]=doit_data;
			console.log("ERERERERERRE");
			console.log((prefix_file+path.parse(file).name));
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






  save_node_graph: function (graph_info_json, dnk_project_path) {
    context=graph_info_json['context'];
    graph_dict=graph_info_json['graph'];


    const fs = require('fs');
  	const path = require('path');



    dnk_struct_array=[ 'prj' , 'ctx' ];

    full_navi_path=dnk_project_path+'/'+ context;
    navi_dir_array=context.split('/');
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

    var struct_dict={};
    var struct_depth={};
    i=0;
    navi_dir_array.forEach(current_dir => {
        struct_dict[dnk_struct_array[i]]=current_dir;
        struct_depth[dnk_struct_array[i]]=i;
        i=i+1;
    });

    save_depth = navi_dir_array.length-1;
    console.log(dnk_struct_array);
    console.log(save_depth);
    console.log(struct_dict);
    console.log(struct_depth);

    Object.entries(graph_dict).forEach(([key, value]) => {
        doit_array=key.split(']');
        doit_name=doit_array[1];
        doit_space=doit_array[0].replace('[','');
        if (struct_depth[doit_space]==save_depth){
            dbox_path=full_navi_path+'/'+doit_name+'.doit';
            console.log(dbox_path);
            let doit_data={}
            if (fs.existsSync(dbox_path)){
                let rawdata = fs.readFileSync(dbox_path);
                doit_data = JSON.parse(rawdata);
			}
			else{
			    doit_data={}
			}

            doit_data['coord']=graph_dict[key]['coord']


            var childs=graph_dict[key]['children_node'];
            var parents=graph_dict[key]['parent_node'];
            console.log(childs,parents);
            childs.forEach(child =>{
                child_array=child.split(']');
                child_name=child_array[1];
                child_space=child_array[0].replace('[','');
                child_depth=struct_depth[child_space];
                if (child_depth<save_depth){
                    var override_data={};
                    var override_path=full_navi_path+'/'+child+'.doit';
                    var override_parents=graph_dict[child]['parent_node'];

                    override_data['inputs'] = override_parents;
                    fs.writeFileSync(override_path, JSON.stringify(override_data, null, 4));
                    console.log("create_override",child,override_parents);
                }

            });
            doit_data['inputs']=parents

            console.log('doit_data');
            fs.writeFileSync(dbox_path, JSON.stringify(doit_data, null, 4))
            console.log(doit_data);

        }
    });
    return graph_info_json;

  }




}





var zemba = function () {

}