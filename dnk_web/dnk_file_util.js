







module.exports = {



  get_graph_info: function (resp_out , dnk_project_path , navi_dir) {

  	const fs = require('fs')
  	const path = require('path');
    var flatten = require('flat')
    var unflatten = require('flat').unflatten

    let dnk_struct_array=[ 'prj' , 'ctx' ];

  	full_navi_path=dnk_project_path+'/'+ navi_dir
    navi_dir_array=navi_dir.split('/')
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
    max_depth=dnk_struct_array.length-1;



    resp_out["its_fin_context"]=0;
    if(max_depth==current_depth){
        //its final context
        //get all all context objects
        folder=dnk_project_path;
        sheets_array=[];
        filesh=[];
        a=0
        for(var i=0; i<navi_dir_array.length;i++){
            folder=folder+'/'+navi_dir_array[a];
            filesh=fs.readdirSync(folder , { withFileTypes: true }).filter(d => d.isFile()).map(d => d.name).map(function(a){ if (a.split('.').slice(-1) == "sheet") return (cur_dnk_path +'/'+ a ); });
            for(var c=0;c<filesh.length;c++){
                if(filesh[c] !== undefined){
                    if ((filesh[c].indexOf("[") != -1) && (filesh[c].indexOf("]") != -1)){
                        sheets_array.push(filesh[c]);
                    }
                    else{
                        sheets_array.push('['+dnk_struct_array[a]+']'+filesh[c].split('/').slice(-1));
                    }
                }
            }

            a=a+1;
        }
        console.log("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE");
        console.log(sheets_array);
        resp_out["sheets"]=sheets_array;
        resp_out["its_fin_context"]=1;
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

    const dbox={};
    const doit={};
    i=0;
    for ( a=0 ; a<all_files_array.length ; a++ ){

        file=all_files_array[a];
	    check_override=file.split(']');
	    if(check_override.length>1){
	        i=i+1;
	        continue;
	    }

		file_path=dnk_project_path+'/'+file;


        prefix_file=all_files_array_name[i];
        clean_prefix=prefix_file.replace('[','').replace(']','');
        doit_depth=dnk_struct_array.indexOf(clean_prefix);

        if (path.extname(file) == ".doit"){

            let rawdata = fs.readFileSync(file_path);
            let doit_data = JSON.parse(rawdata);

            //res_data=flatten(doit_data);
            res_data=doit_data;
            res_data['over']=0;

            //console.log(file_path);
            // OVERRIDE SEARCH
            if (doit_depth < current_depth){
                res_data['depth']=0.65;
                var mypath=dnk_project_path+path.dirname(file);
                for(let it=doit_depth+1 ; it<current_depth+1; it++){

                    mypath=mypath+'/'+navi_dir_array[it];
                    override_name=mypath+'/'+prefix_file+path.basename(file);
                    if (fs.existsSync(override_name)){
                        res_data['over']=1;

                        let over_rawdata = fs.readFileSync(override_name);
                        let over_doit_data = JSON.parse(over_rawdata);
                        if('inputs' in over_doit_data){
                            res_data['inputs']= Array.from(new Set( res_data['inputs'].concat(over_doit_data['inputs']) ));

                        }
                        else{console.log('No Input');}


                    }
                }

            }
            doit[(prefix_file+path.parse(file).name)]=res_data;

        }



		if (path.extname(file) == ".dbox"){

            let rawdata = fs.readFileSync(file_path);
            let dbox_data = JSON.parse(rawdata);

            //res_data=flatten(dbox_data);
            res_data=dbox_data;
            res_data['over']=0;

            //console.log(file_path);
            // OVERRIDE SEARCH
            if (doit_depth < current_depth){
                res_data['depth']=0.65;
                var mypath=dnk_project_path+path.dirname(file);
                for(let it=doit_depth+1 ; it<current_depth+1; it++){

                    mypath=mypath+'/'+navi_dir_array[it];
                    override_name=mypath+'/'+prefix_file+path.basename(file);
                    if (fs.existsSync(override_name)){
                        res_data['over']=1;

                        let over_rawdata = fs.readFileSync(override_name);
                        let over_doit_data = JSON.parse(over_rawdata);
                        if('inputs' in over_doit_data){
                            res_arr=[]
                            for (var rule_name in res_data['de_rules']) {
                                res_arr.push(res_data['de_rules'][rule_name]['doit']);

                            }
                            res_data['inputs']= Array.from(new Set( res_arr ));

                        }
                        else{console.log('No Input');}


                    }
                }

            }
            dbox[(prefix_file+path.parse(file).name)]=res_data;



			//dbox.push(path.parse(file).name);
			}
		i=i+1;
	}

	resp_out["doit_arr"]=doit;
	resp_out["dbox_arr"]=dbox;

    //console.log('REEEEEEEEEEEEEEEEEEEEEEESPPPPPPPPP');
    console.log(resp_out);
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
    //console.log(dnk_struct_array);
    //console.log(save_depth);
    //console.log(struct_dict);
    //console.log(struct_depth);



    Object.entries(graph_dict).forEach(([key, value]) => {
        doit_array=key.split(']');
        doit_name=doit_array[1];
        doit_space=doit_array[0].replace('[','');

        if (struct_depth[doit_space]==save_depth){
            dbox_path=full_navi_path+'/'+doit_name+'.doit';

            if(graph_dict[key]['node_type']=='dbox_node'){
                dbox_path=full_navi_path+'/'+doit_name+'.dbox';
            }
            
            //console.log(dbox_path);
            let doit_data={}
            if (fs.existsSync(dbox_path)){
                let rawdata = fs.readFileSync(dbox_path);
                doit_data = JSON.parse(rawdata);
			}
			else{
			    doit_data={}
			}

            doit_data['coord']=graph_dict[key]['coord']

            if(graph_dict[key]['node_type']=='dbox_node'){
                fs.writeFileSync(dbox_path, JSON.stringify(doit_data, null, 4));
                return;

            }
            

            var childs=graph_dict[key]['children_node'];
            var parents=graph_dict[key]['parent_node'];
            //console.log(childs,parents);
            childs.forEach(child =>{
                child_array=child.split(']');
                child_name=child_array[1];
                child_space=child_array[0].replace('[','');
                child_depth=struct_depth[child_space];
                if (child_depth<save_depth){
                    var override_data={};
                    var override_path=full_navi_path+'/'+child+'.doit';
                    var override_parents_in=graph_dict[child]['parent_node'];

                    override_parents=[];

                    override_parents_in.forEach(cur_parent =>{
                        cur_parent_array=cur_parent.split(']');
                        cur_parent_name=cur_parent_array[1];
                        cur_parent_space=cur_parent_array[0].replace('[','');
                        cur_parent_depth=struct_depth[cur_parent_space];

                        if (cur_parent_depth==save_depth){
                            override_parents.push(cur_parent);
                        };

                    });

                    override_data['inputs'] = override_parents;
                    fs.writeFileSync(override_path, JSON.stringify(override_data, null, 4));
                    console.log("create_override",child,override_parents);
                }

            });
            doit_data['inputs']=parents

            //console.log('doit_data');
            fs.writeFileSync(dbox_path, JSON.stringify(doit_data, null, 4))
            //console.log(doit_data);

        }
    });



    return graph_info_json;

  },






  garbage_collector: function (graph_info_json, dnk_project_path) {

        context=graph_info_json['context'];
        graph_dict=graph_info_json['graph'];

        const fs = require('fs');
        const path = require('path');
        var glob = require('glob');


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




        glob_overrides=full_navi_path+'/[*';
        files_o=glob.sync(glob_overrides);
        console.log('files_o');
        console.log(files_o);



        files_o.forEach(over_file => {
            node_name=path.basename(over_file).replace(/\.[^/.]+$/, "");
            let override_file = fs.readFileSync(over_file);
            let over_data = JSON.parse(override_file);
            console.log('over_node_name');
            console.log(node_name);
            if('inputs' in over_data){
                in_arr=over_data['inputs'];
                in_arr.forEach(inpts => {
                    node_in_graph=graph_dict[inpts];
                    children_nodes= node_in_graph['children_node'];
                    if (children_nodes.indexOf(node_name) > -1){
                        console.log('Yes Array');
                        console.log(over_data);
                    }
                    else{
                        console.log('No Array');
                        delete_index=over_data['inputs'].indexOf(inpts);
                        over_data['inputs'].splice(over_data['inputs'].indexOf(inpts));
                        if (over_data['inputs'].length==0) {
                            delete over_data['inputs'];
                            if(Object.keys(over_data).length === 0){
                                console.log('REMOVE_FILE_OVERRIDE');
                                fs.unlinkSync(over_file);
                            }
                        }

                    }

                });
            }
        });





        return 1;

    },





    add_doit: function (doit_data) {
        const fs = require('fs');
        const path = require('path');
        var glob = require('glob');

        var out_doit_data={};
        var doit_create_path=doit_data.create_doit_path+'/';
        var dnk_project_path=doit_data.dnk_project_path+'/';

        out_doit_data["coord"]=doit_data.cam_coord;
        out_doit_data["annotation"]=doit_data.out_doit_annotation
        if (doit_create_path.replace(/\/+/gi,'/')==dnk_project_path.replace(/\/+/gi,'/')){
            return "Out project space -> No Create DoIt ";
        }
        else{
            doit_path=doit_create_path.replace(/\/+/gi,'/')+doit_data.out_doit_name+'.doit'
            if (fs.existsSync(doit_path)){
                return "File_exist -> No Create DoIt";
            }
            else{
                fs.writeFileSync(doit_path, JSON.stringify(out_doit_data, null, 4))
                return "Create DoIt successful";
            }

        }




    }










}





var zemba = function () {

}