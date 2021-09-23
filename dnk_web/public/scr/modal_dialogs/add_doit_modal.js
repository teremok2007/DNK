var modal = document.getElementById("base_modal");
var modal_content = document.getElementById("modal_content");
var add_doit_btn = document.getElementById("add_doit");






 add_doit_btn.onclick = function () {

    modal_content.innerHTML = '';
    var in_doit_name = document.createElement('div');
    in_doit_name.id = 'in_doit_annotation';
    in_doit_name.innerHTML =     "<strong>DoIt Name   :</strong><input type='text' value='' class='modal_item' id='in_doit_name'  style='padding:5px;' /> ";
    modal_content.append(in_doit_name);


    var doit_annotation = document.createElement('div');
    in_doit_annotation.id = 'in_doit_annotation';
    doit_annotation.innerHTML =     "<p><b>Annotation:</b></p><textarea rows=\"12\" cols = \"47\" class='in_doit_annotation'  id='in_doit_annotation'</textarea>";
    modal_content.append(doit_annotation);

    var add_doit_ok_btn = document.createElement('div');
    add_doit_ok_btn.id = 'add_doit_ok_btn';
    add_doit_ok_btn.innerHTML = "<button type='button' id='add_doit_ok_btn' class='modal_btn'>Create</button> ";
    modal_content.append(add_doit_ok_btn);


    modal_content.style.height="400px";
    modal.style.display = "flex";

 }



  window.onclick = function (event) {
    if (event.target == modal) {
        modal_content.innerHTML = '';
        //document.getElementById("in_doit_name").value='';
        //document.getElementById("in_doit_annotation").value='';
        modal.style.display = "none";
    }
}