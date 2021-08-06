$(document).ready(function()
{
            var addEvent = function(object, type, callback) {
                if (object == null || typeof(object) == 'undefined') return;
                if (object.addEventListener) {
                    object.addEventListener(type, callback, false);
                } else if (object.attachEvent) {
                    object.attachEvent("on" + type, callback);
                } else {
                    object["on"+type] = callback;
                }
            };


            addEvent(window, "resize", function(event) {

              console.log('resized');
              resizeCanvas();
            });





            var wp = document.getElementById("type_wp");

            wp.addEventListener("click",function (e){
                var navi_brwsr = document.getElementById("navi_browser");
                var file_brwsr = document.getElementById("file_browser");
                var type_navi = document.getElementById("type_navi");
                this.style.boxShadow ="0px 0px 10px 0px #ffffff inset";
                type_navi.style.boxShadow ="0px 0px 0px 0px #ffffff";

                navi_brwsr.style.display="none";
                file_brwsr.style.display="block";
            });



            var navi = document.getElementById("type_navi");

            navi.addEventListener("click",function (e){
                var navi_brwsr = document.getElementById("navi_browser");
                var file_brwsr = document.getElementById("file_browser");
                var type_wp = document.getElementById("type_wp");
                this.style.boxShadow ="0px 0px 10px 0px #ffffff inset";
                type_wp.style.boxShadow ="0px 0px 0px 0px #ffffff";

                navi_brwsr.style.display="block";
                file_brwsr.style.display="none";
            });





            var iter_start_out = document.getElementById("it_start_out_btn");

            iter_start_out.addEventListener("mousedown",function (e){

                        this.style.backgroundColor="#AB7810";
                        var node=GetActiveNodes();
                        active_iter_folder=myIterFolders;
                        arr_fold=[]
                        for(var i=0;i<active_iter_folder.length;i++){
                            arr_fold.push(document.getElementById(active_iter_folder[i]).dataset.id.replaceAll("//", "/"));
                        }


                        console.log(arr_fold);
                        
                        out_dict={};
                        out_dict['path_node']=node;
                        out_dict['iterator']=arr_fold;
                        let select_node = JSON.stringify(out_dict);

                        let request = new XMLHttpRequest();
                        request.open("POST", "/start_up", true);
                        request.setRequestHeader("Content-Type", "application/json");

                        request.send(select_node);

                        //console.log(data_path);*/

            });


            iter_start_out.addEventListener("mouseup",function (e){

                        this.style.backgroundColor="#EFA614";


            });





});
