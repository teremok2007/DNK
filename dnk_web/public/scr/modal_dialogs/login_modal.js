var modal = document.getElementById("base_modal");
var modal_content = document.getElementById("modal_content");
var btn = document.getElementById("sign_in_btr");
var lvl = document.getElementById("super_level");
var svgrph = document.getElementById("save_graph");
var adddoit = document.getElementById("add_doit");
var user_mode = document.getElementById("user_mode");
var left_win = document.getElementById("main_browser");
var right_win = document.getElementById("right_browser");
var navi_win = document.getElementById("navigator");
var main_menu = document.getElementById("main_menu");

var span = document.getElementsByClassName("close_modal_window")[0];



left_win.style.display="none";
right_win.style.display="none";
navi_win.style.display="none";

user_mode.style.display="none";
svgrph.style.display="none";
adddoit.style.display="none";
modal.style.display="none";



var in_mail = document.createElement('div');
in_mail.id = 'in_mail';

in_mail.innerHTML =     "<strong>Mail   :</strong><input type='text' value='' class='modal_item' id='modal_mail'  style='padding:5px;' /> ";
modal_content.append(in_mail);

var in_password = document.createElement('div');
in_password.id = 'in_password';
in_password.innerHTML = "<strong>Password :</strong> <input type='password' value='' class='modal_item' id='modal_password'  style='padding:5px;' /> ";
modal_content.append(in_password);

var sign_in = document.createElement('div');
sign_in.id = 'sign_in';
sign_in.innerHTML = "<button type='button' id='modal_btn' class='modal_btn'>Sing In</button> ";
modal_content.append(sign_in);


var out_text = document.createElement('div');
out_text.id = 'out_text';
out_text.style.color='red';
out_text.style.display='none';
out_text.style.margin='0 140px';
out_text.innerHTML = "INCORRECT";
modal_content.append(out_text);


main_menu.style.display='none';
modal.style.display = "flex";
out_text.style.display='none';
document.getElementById("modal_mail").value='';
document.getElementById("modal_password").value='';

modal_btn=document.getElementById("modal_btn");


modal_btn.onclick = function () {

    var mail_in = document.getElementById("modal_mail").value;
    var pass_in = document.getElementById("modal_password").value;

    let user_info = JSON.stringify({ "mail": mail_in, "password" : pass_in });

    let request = new XMLHttpRequest();
    request.open("POST", "/user_validate", true);
    request.setRequestHeader("Content-Type", "application/json");




    request.addEventListener("load", function () {
        let user_info = JSON.parse(request.response);
        var name_in=user_info.name;
        var super_in=user_info.super;

        if (name_in=='none'){
            out_text.style.display='flex';
        }
        else
        {
            left_win.style.display="block";
            right_win.style.display="flex";
            navi_win.style.display="flex";
            main_menu.style.display='flex';
            modal.style.display = "none";
            btn.textContent = name_in;
            lvl.textContent = super_in;


            if (super_in==0){
                svgrph.style.display="none";
                adddoit.style.display="none";
                user_mode.style.display="block";
            }
            else{
                svgrph.style.display="block";
                adddoit.style.display="block";
                user_mode.style.display="block";
            }
        }

        console.log(name_in);
        console.log(super_in);
    });


    request.send(user_info);



    //modal.style.display = "none";
 }



 btn.onclick = function () {
    modal.style.display = "flex";
    out_text.style.display='none';
    document.getElementById("modal_mail").value='';
    document.getElementById("modal_password").value='';
 }

 span.onclick = function () {
    out_text.style.display='none';
    document.getElementById("modal_mail").value='';
    document.getElementById("modal_password").value='';
    modal.style.display = "none";

 }

 window.onclick = function (event) {
    if (event.target == modal) {
        document.getElementById("modal_mail").value='';
        document.getElementById("modal_password").value='';
        modal.style.display = "none";
    }
}