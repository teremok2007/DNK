module.exports = {

  get_graph_info: function (resp_out , navi_folder , proj) {

  	const fs = require('fs')
  	const path = require('path');

    dirs = fs.readdirSync(navi_folder , { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name);
    files = fs.readdirSync(navi_folder , { withFileTypes: true }).filter(d => d.isFile()).map(d => d.name);
    resp_out["files_arr"]=files;
    resp_out["dir_arr"]=dirs;

    const dbox=[];
    const doit={};

	files.forEach(file => {
		file_path=proj+resp_out['root']+'/'+file;
		console.log(file_path);

		if (path.extname(file) == ".doit"){
			
			let rawdata = fs.readFileSync(file_path);
			let doit_data = JSON.parse(rawdata);
			doit[path.parse(file).name]=doit_data;
		}

		if (path.extname(file) == ".dbox")
			dbox.push(path.parse(file).name);
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