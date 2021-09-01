$(document).ready(function()
{



        project_name="";
        folder_depth=0;

        let get_files = JSON.stringify({directory: project_name , parent_name: "navi_browser" ,depth_folder:folder_depth});

        let request = new XMLHttpRequest();
        request.open("POST", "/get_navi_files", true);
        request.setRequestHeader("Content-Type", "application/json");


        
        
        request.addEventListener("load", function () {

            let files = JSON.parse(request.response);

            NodeUpdate(files);

            var node = document.getElementById(files.parent);
            dir_array=files.dir_arr;
            files_array=files.files_arr;
            proj_relative_path=files.root;
            in_depth=files.depth;

            var parent=document.getElementById(files.parent).dataset.id;


            if (in_depth>12 && parent) {
                var out_to_it=parent.replace(/_navi_box/gi,'').split('/').filter(val => val !== "");
                IteratorUpdate(out_to_it[0], out_to_it[1]);
            }
            else{
                IteratorUpdate('none', 'none');
            }

            dir_array.forEach(dir_in => {
                let dir = document.createElement('div');

                dir.className = "navi_column_folder";
                dir.id="cn_"+proj_relative_path+"/"+dir_in;
                dir.dataset.id=proj_relative_path+"/"+dir_in;
                dir.dataset.open=0;
                dir.dataset.depth=in_depth;
                dir.dataset.select=0;
                dir.innerHTML = "<div> <div class=\"space\" style=\"padding-left:"+in_depth+"px\"><\div> <img src=\"/public/icons/folder/keyboard_arrow_right-12px.svg\"> <img src=\"/public/icons/folder/folder-12px.svg\"> " + dir_in +"</div>";
                node.append(dir);

                let dir_box = document.createElement('div');
                dir_box.className = "navi_folder_box";
                dir_box.id="cn_"+proj_relative_path+"/"+dir_in+"_navi_box";
                dir_box.dataset.id=proj_relative_path+"/"+dir_in+"_navi_box";
                dir_box.dataset.open=0;
                node.append(dir_box);

                dir.addEventListener("dblclick",function (e){
                    
                    new_path=this.dataset.id;
                    parent_path="cn_"+this.dataset.id+"_navi_box";


                    if(this.dataset.open==1)
                    {
                        this.dataset.open=0;
                        var folder_box = document.getElementById(parent_path);
                        //alert(parent_path);
                        folder_box.innerHTML = '';
                        this.innerHTML = "";
                        this.innerHTML = "<div> <div class=\"space\" style=\"padding-left:"+this.dataset.depth+"px\"><\div> <img src=\"/public/icons/folder/keyboard_arrow_right-12px.svg\"> <img src=\"/public/icons/folder/folder-12px.svg\"> " + dir_in +"</div>";

                        return 1;
                    }
                    else if (this.dataset.open==0) {
                        this.dataset.open=1;
                    }
                    this.innerHTML = "";
                    this.innerHTML = "<div> <div class=\"space\" style=\"padding-left:"+this.dataset.depth+"px\"><\div> <img src=\"/public/icons/folder/keyboard_arrow_down-12px.svg\"> <img src=\"/public/icons/folder/folder-12px.svg\"> " + dir_in +"</div>";
                    folder_depth=parseInt(this.dataset.depth)+12;
                    let get_dir = JSON.stringify({directory: new_path , parent_name :parent_path ,depth_folder:folder_depth});

                    request.open("POST", "/get_navi_files", true);
                    request.setRequestHeader("Content-Type", "application/json");

                    request.send(get_dir);
                    //alert(new_path);
                });






                dir.addEventListener("click",function (e){
                    if (e.altKey) {
                        
                        nav_prj=this.dataset.id;
                        in_projects=nav_prj;
                        navigator_update(in_projects);
                        navigator_clear_selection();
                        navigator_add_selection(this.id);
                    }



                    else if (e.shiftKey) {


                        if (this.dataset.select==0){
                            this.dataset.select=1;
                            this.style.backgroundColor ="#eaeaea";
                            navigator_add_selection(this.id);



                        }
                        else {
                            this.dataset.select=0;
                            this.style.backgroundColor ="#88c6eb";
                        }
                    }

                    else {

                        navigator_clear_selection();
                        navigator_add_selection(this.id);
                    }

                });









            });


        });


        request.send(get_files);


























});
