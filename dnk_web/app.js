
const express = require("express");
const handlebars = require('express-handlebars');
var jquery = require('jquery');
var f_utl = require('./dnk_file_util');
const app = express();

app.engine('handlebars', handlebars({defaultLayout: 'main'}));
app.set('views', './views');
app.set('view engine', 'handlebars');

app.use('/public',express.static(__dirname + '/public'));

app.get('/', (req, res) => {
    console.log("START");
    console.log(req);
    res.render('home', {title: 'Greetings form Handlebars'});
    console.log("RES");
    console.log(res);
});
const jsonParser = express.json();


const fs = require('fs')
var path = require('path')

var dnk_init_json_path = path.join(__dirname, '..', 'dnk_init.json');
var dnk_path = path.join(__dirname, '..');
const dnk_json_init = require(dnk_init_json_path);

const dnk_python_path = (dnk_path+"/dnk_master/dnk_core/python/").replace(/\\/gi,'/');
const dnk_project_path = (dnk_path+"/dnk_master/dnk_proj/").replace(/\\/gi,'/');
const dnk_user_path = (dnk_path+"/dnk_master/dnk_users/").replace(/\\/gi,'/');
const reel_project_path =(dnk_json_init['studio_proj_root']).replace(/\\/gi,'/');




app.post("/add_doit", jsonParser, function (request, response) {
    if(!request.body) return response.sendStatus(400);
    console.log(request);
    body=request.body;
    doit_name=body.doit_name;
    doit_annotation=body.doit_annotation;
    doit_coord=body.cam_coord
    create_doit_path=dnk_project_path+'/'+body.moni_name;
    out_dict={ "out_doit_name": doit_name, "out_doit_annotation" : doit_annotation , "create_doit_path" : create_doit_path, "dnk_project_path":dnk_project_path , "cam_coord":body.cam_coord };
    duits=f_utl.add_doit(out_dict)
    console.log(duits);
    response.json(duits);

});









app.post("/user_validate", jsonParser, function (request, response) {
    console.log(request.body);
    if(!request.body) return response.sendStatus(400);

    user_init_path=dnk_user_path+'/_init_';
    console.log(user_init_path)
    let user_init_file = fs.readFileSync(user_init_path);
    let user_init_data = JSON.parse(user_init_file);
    let user_mails=Object.keys(user_init_data.users_map);


    out={name : 'none' , super:'none'};

    body=request.body;
    mail=body.mail;
    pass=body.password;

    user_mails.forEach(current_mail => {

        if (mail==current_mail){
            console.log(mail);
            var mail_data=user_init_data.users_map[current_mail];
            password_data=mail_data.password;
            console.log(password_data);
            console.log(pass);
            if (pass==password_data){
                out={ name : mail_data.name , super : mail_data.super };
            }

        }

    });

    console.log(out);
    response.json(out);
});




app.post("/node_save_graph", jsonParser, function (request, response) {
    console.log(request.body);
    if(!request.body) return response.sendStatus(400);

    node_graph_info=request.body;
    f_utl.garbage_collector(node_graph_info,dnk_project_path);
    response_body=f_utl.save_node_graph(node_graph_info,dnk_project_path);
    response.json(response_body);
});




app.post("/get_files", jsonParser, function (request, response) {
    console.log(request.body);
    if(!request.body) return response.sendStatus(400);

    body=request.body;
    const folderPath = reel_project_path+"/"+body.directory;
    relative_path=body.directory;
    parent_node_name=body.parent_name;
    folder_depth=body.depth_folder;

    dirs = fs.readdirSync(folderPath , { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name);
    files = fs.readdirSync(folderPath , { withFileTypes: true }).filter(d => d.isFile()).map(d => d.name);
    out = { dir_arr: dirs , files_arr: files , root: relative_path ,parent: parent_node_name , depth:folder_depth};
    console.log(out);
    response.json(out);
});


app.post("/get_navi_files", jsonParser, function (request, response) {
    console.log(request.body);
    if(!request.body) return response.sendStatus(400);

    navi_body=request.body;
    const navi_folderPath = dnk_project_path+"/"+navi_body.directory;

    var out = {};

    // Create Context Folders If Folders Exists
    if (navi_body.depth_folder==12){

        proj_init_path=navi_folderPath+'/_init_';

        let init_file = fs.readFileSync(proj_init_path);
        let init_data = JSON.parse(init_file);
        let contexts=Object.keys(init_data.contexts);

        contexts.forEach(current_ctx => {
            make_dir=navi_folderPath+'/' + current_ctx;
            if (!fs.existsSync(make_dir)){
                fs.mkdirSync(make_dir);
            };
        });
    }

    out['root']=navi_body.directory;
    out['parent']=navi_body.parent_name;
    out['depth']=navi_body.depth_folder;
    out['doit_arr']={};
    out['dbox_arr']=[];
    //console.log(navi_folderPath);
    fin_out=f_utl.get_graph_info(out,dnk_project_path, navi_body.directory);


    console.log(fin_out);
    response.json(fin_out);
});


app.post("/get_dir", jsonParser, function (request, response) {
    console.log(request.body);
    if(!request.body) return response.sendStatus(400);

    body = request.body;
    const folderPath = dnk_project_path +"/"+ body.directory;
    const projPath=body.directory;

    dirs = fs.readdirSync(folderPath , { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name);
    out = { files_arr: dirs , root_path:projPath};
    console.log(out);
    response.json(out);
});


app.post("/get_iterator", jsonParser, function (request, response) {

    const spawn = require('child_process').spawn;

    console.log(request.body);

    if(!request.body) return response.sendStatus(400);

    iter_body=request.body;

    const iterator_name = iter_body.iterator;
    const proj = iter_body.proj;
    const context = iter_body.context;

    var out = {};
    var dataToSend='';
    iter_name=dnk_python_path+'/iterators/'+ iterator_name + '.py';
    console.log(iter_name);

    const python = spawn('python',[iter_name, proj, context]);

    python.stdout.on('data', function(data) {
        dataToSend = dataToSend+data.toString();
    } );
    python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);

    res_send={};
    if(response) {
        try {
            res_send=JSON.parse(dataToSend);
        }
        catch(e) {
            console.log(e);
        }
    }

     response.json(res_send);
     });

});


app.post("/start_up", jsonParser, function (request, response) {

    const fs = require('fs');
    const spawn = require('child_process').spawn;

    console.log(request.body);
    if(!request.body) return response.sendStatus(400);

    body = request.body;
    let file_node=dnk_project_path+body['path_node']+'.doit';
    let iterator=JSON.stringify( body['iterator'] )
    console.log(file_node);
    console.log(iterator);

    let rawdata = fs.readFileSync(file_node);
    let doit_data = JSON.parse(rawdata);
    let python_run_path=dnk_python_path+'/dnk_run.py'

    const pythonProcess = spawn('python',[python_run_path, file_node ,iterator]);
    process.stdout.on('data', function(data) {
        res.send(data.toString());
        console.log(data.toString());
    } )
    //console.log(body['path_node']);
    console.log(doit_data);
    console.log(file_node);
    console.log(iterator);
    response.ok;
});















app.listen(3000);
