var modal = document.getElementById("base_modal");
var modal_content = document.getElementById("modal_content");
var add_doit_btn = document.getElementById("add_doit");






 add_doit_btn.onclick = function () {

    modal_content.innerHTML = '';
    var doit_name = document.createElement('div');
    doit_name.id = 'in_doit_name_div';
    doit_name.innerHTML =     "<strong>DoIt Name   :</strong><input type='text' value='' class='modal_item' id='in_doit_name'  style='padding:5px;' /> ";
    modal_content.append(doit_name);


    var doit_annotation = document.createElement('div');
    doit_annotation.id = 'in_doit_annotation_div';
    doit_annotation.innerHTML =     "<p><b>Annotation:</b></p><textarea rows=\"12\" cols = \"47\" class='in_doit_annotation'  id='in_doit_annotation'</textarea>";
    modal_content.append(doit_annotation);

    var add_doit_ok_btn = document.createElement('div');
    add_doit_ok_btn.id = 'add_doit_ok_btn_div';
    add_doit_ok_btn.innerHTML = "<button type='button' id='add_doit_ok_btn' class='modal_btn'>Create</button> ";
    modal_content.append(add_doit_ok_btn);


    modal_content.style.height="400px";
    modal.style.display = "flex";


    add_doit_ok_btn.onclick = function () {

        var my_node_canvas = document.getElementById("canvas").value;

        var doit_name_val = document.getElementById("in_doit_name").value;
        var doit_annotation_val = document.getElementById("in_doit_annotation").value;
        var moni_info=NodeMonitorDnkCanvasInfo();

        let add_doit_info = JSON.stringify({ "doit_name": doit_name_val, "doit_annotation" : doit_annotation_val , "moni_name" : moni_info.moni_name , "cam_coord" : moni_info.cam_coord});

        let request = new XMLHttpRequest();
        request.open("POST", "/add_doit", true);
        request.setRequestHeader("Content-Type", "application/json");




        request.addEventListener("load", function () {
            let doit_out_info = JSON.parse(request.response);
            navigator_update(moni_info.moni_name);

            modal_content.innerHTML = '';
            modal.style.display = "none";

        });

        request.send(add_doit_info);

    }

 }



  window.onclick = function (event) {
    if (event.target == modal) {
        modal_content.innerHTML = '';
        modal.style.display = "none";
    }
}