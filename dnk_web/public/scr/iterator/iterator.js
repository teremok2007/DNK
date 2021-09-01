function IteratorUpdate(proj,context){

        console.log("ITERATOR_WORK");


        project_name="";
        folder_depth=0;

        let get_files = JSON.stringify({ "iterator": "dnk_main_context_it", "proj":proj, "context":context });

        let request = new XMLHttpRequest();
        request.open("POST", "/get_iterator", true);
        request.setRequestHeader("Content-Type", "application/json");




        request.addEventListener("load", function () {

            let files = JSON.parse(request.response);

            console.log(files);
            document.getElementById('iterator').innerHTML = "";
            var node = document.getElementById('iterator');
            iter_array=files.iter.sort();

            n=0;
            iter_array.forEach(dir_in => {
                let dir = document.createElement('div');

                dir.className = "iterator_folder";
                dir.id="it_/"+dir_in;
                dir.dataset.id="/"+dir_in;
                dir.dataset.n=n;
                dir.dataset.open=0;
                dir.dataset.depth=in_depth;
                dir.dataset.select=0;
                dir.innerHTML = "<div> <div class=\"space\" style=\"padding-left:12px\"><\div> <img src=\"/public/icons/folder/folder-12px.svg\"> " + dir_in +"</div>";
                node.append(dir);
                n=n+1;
                let dir_box = document.createElement('div');
                dir_box.className = "iterator_box";
                dir_box.id="it_/"+dir_in+"_iter_box";
                dir_box.dataset.id="/"+dir_in+"_iter_box";
                dir_box.dataset.open=0;
                node.append(dir_box);


                dir.addEventListener("dblclick",function (e){
                    return 1;
                });

                dir.addEventListener("click",function (e){
                    if (e.ctrlKey) {
                        if (this.dataset.select==0){
                            this.dataset.select=1;
                            this.style.backgroundColor ="#eaeaea";
                            iterator_add_selection(this.id);
                        }
                        else {
                            this.dataset.select=0;
                            this.style.backgroundColor ="#C7E495";
                        }
                    }
                    else if (e.shiftKey){
                      iterator_add_shift_selection(this.id);
                    }
                    else {
                        iterator_clear_selection();
                        iterator_add_selection(this.id);
                        this.dataset.select=1;
                    }
                });









            });


        });


        request.send(get_files);


};
