function navigator_update(nav_path) {



    //let nav_prj="";
    let nav_prj=nav_path
    let get_dir = JSON.stringify({directory: nav_prj});

    let request = new XMLHttpRequest();
    request.open("POST", "/get_navi_files", true);
    request.setRequestHeader("Content-Type", "application/json");


    

    request.addEventListener("load", function () {

        
        let files = JSON.parse(request.response);

        NodeUpdate(files);

        var node = document.getElementById("navigator");
        node.innerHTML = '';
        files_array=files.dir_arr;
        root_dir=files.root;

        files_array.forEach(file_in => {
            let file = document.createElement('div');
            file.className = "navi_folder";
            file.id ="n_"+file_in;
            file.dataset.id = file_in;
            file.dataset.root = root_dir;
            file.innerHTML = "<div>" +file_in +" </div>";
            node.append(file);

            file.addEventListener("dblclick",function (e){

              new_path=this.dataset.root+"/"+this.dataset.id;

              document.title=new_path;
              let get_dir = JSON.stringify({directory: new_path});

              request.open("POST", "/get_navi_files", true);
              request.setRequestHeader("Content-Type", "application/json");
              request.send(get_dir);
              
            });

        });

    });


    request.send(get_dir);



};










var mySelectFolders=[];


function navigator_add_selection(select_id) {
    mySelectFolders.push(select_id);
    var sel_fldr = document.getElementById(select_id);
    sel_fldr.style.backgroundColor ="#eaeaea";
};


function navigator_clear_selection() {
    mySelectFolders.forEach(folder_id => {
        var sel_fldr = document.getElementById(folder_id);
        sel_fldr.style.backgroundColor ="#88c6eb";
    });
    mySelectFolders=[];
};
