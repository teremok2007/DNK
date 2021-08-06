
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
    res.render('home', {title: 'Greetings form Handlebars'});
    //console.log(res)
});



//app.use(express.json({ limit: 100000000 }));



const fs = require('fs')
const path = require('path')
const jsonParser = express.json();


const dnk_py_path = "R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/python/";
const dnk_project_path = "R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper_proj/";
const reel_project_path ="R:/01_Projects/";




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

    out['root']=navi_body.directory;
    out['parent']=navi_body.parent_name;
    out['depth']=navi_body.depth_folder;
    out['doit_arr']={};
    out['dbox_arr']=[];
    console.log(navi_folderPath);
    fin_out=f_utl.get_graph_info(out,navi_folderPath,dnk_project_path);


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

    var out = {};
    var dataToSend='';
    iter_name=dnk_py_path+'/iterators/'+ iterator_name + '.py';
    console.log(iter_name);
    const python = spawn('python',[iter_name]);
    python.stdout.on('data', function(data) {

        dataToSend = dataToSend+ data.toString();

    } )
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);

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

    const pythonProcess = spawn('python',["R:/01_Projects/Dog/production/exchange/a_bocharov/DNK/cooper/cooper/python/dnk_run.py", file_node ,iterator]);
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
