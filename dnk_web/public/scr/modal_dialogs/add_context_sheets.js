var modal = document.getElementById("base_modal");
var modal_content = document.getElementById("modal_content");
var add_ctx_sheets_btn = document.getElementById("ctx_sheets");






 add_ctx_sheets_btn.onclick = function () {

    modal_content.innerHTML = '';
    var sheet_name = document.createElement('div');
    sheet_name.id = 'in_sheet_name_div';
    sheet_name.innerHTML =     "<strong>Sheet Name   :</strong><input type='text' value='' class='modal_item' id='in_sheet_name'  style='padding:5px;' /> ";
    modal_content.append(sheet_name);



    var sheet_type_get_ctx = document.createElement('div');
    sheet_type_get_ctx.id = 'get_ctx_div';
    sheet_type_get_ctx.innerHTML ='<strong>Get Item Way   :</strong><select id="select_id" class="modal_btn"><option value=hand class="modal_btn">Hand Add Item</option><option value=all class="modal_btn">This Context All Items</option><option value=down class="modal_btn">Down Stream Context Items</option></select>'
    modal_content.append(sheet_type_get_ctx);



    var add_ctx_sheets_ok_btn = document.createElement('div');
    add_ctx_sheets_ok_btn.id = 'add_ctx_sheets_ok_btn_div';
    add_ctx_sheets_ok_btn.innerHTML = "<button type='button' id='add_ctx_sheets_ok_btn' class='modal_btn'>Create Context Sheet</button> ";
    modal_content.append(add_ctx_sheets_ok_btn);


    modal_content.style.height="250px";
    modal.style.display = "flex";


    add_ctx_sheets_ok_btn.onclick = function () {

        var my_node_canvas = document.getElementById("canvas").value;

        var sheet_name_val = document.getElementById("in_sheet_name").value;
        var sheet_ctx_type_val = document.getElementById("select_id").value;
        var moni_info=NodeMonitorDnkCanvasInfo();
        console.log(sheet_name_val);
        console.log(sheet_ctx_type_val);

        let add_doit_info = JSON.stringify({ "sheet_name": sheet_name_val, "sheet_ctx_type" : sheet_ctx_type_val , "moni_name" : moni_info.moni_name });
        console.log(add_doit_info)
        let request = new XMLHttpRequest();
        request.open("POST", "/add_sheets", true);
        request.setRequestHeader("Content-Type", "application/json");




        request.addEventListener("add_sheet", function () {
            let doit_out_info = JSON.parse(request.response);
            //navigator_update(moni_info.moni_name);

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