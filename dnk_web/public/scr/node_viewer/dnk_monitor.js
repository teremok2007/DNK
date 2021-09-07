document.title='DNK';


var canvas = new fabric.Canvas('canvas',{
    perPixelTargetFind: true,
    targetFindTolerance: 5,
    fireRightClick: true,
    fireMiddleClick: true,
    stopContextMenu: true,
});
canvas.hoverCursor = 'pointer';
var pos;
var mouseDownPoint = null;


fabric.Object.prototype.originX = fabric.Object.prototype.originY = 'center';




canvas.off('contextmenu');


canvas.on('mouse:wheel', function(opt) {
    var delta = opt.e.deltaY;


    var pointer = canvas.getPointer(opt.e);
    var zoom = canvas.getZoom();
    zoom = zoom - delta/1000;
    if (zoom > 20) zoom = 20;
    if (zoom < 0.01) zoom = 0.01;
    canvas.zoomToPoint({ x: opt.e.offsetX, y: opt.e.offsetY }, zoom);
    opt.e.preventDefault();
    opt.e.stopPropagation();
});



function resizeCanvas() {

    var height_offset = document.getElementById('navigator').style.height;

    canvas.setWidth( 1300 );
    canvas.setHeight( window.innerHeight-100 );
    canvas.calcOffset();


  }
  resizeCanvas();





canvas.on('mouse:move', function(opt) {
    pos = canvas.getPointer(opt.e);
});




addEventListener("keydown", function(event) {
    if (event.keyCode == 32)
        //document.title=Math.floor(pos.x);
        var nodeA=createNode( Math.floor(pos.x) , canvas , pos.x, pos.y );
});



addEventListener("keydown", function(event) {
    if (event.keyCode == 46)

        var current_obj = canvas.getActiveObject();
        
        if (!current_obj){
            return;
        }
        if (current_obj.type=='arrows')
        {
            deleteArrow(current_obj);
        }
        else
        {
            deleteNode(canvas);
        }


});







addEventListener("keydown", function(event) {
    var out='Child:';
    if (event.keyCode == 73)
        var out_obj = canvas.getActiveObject();
        if (!out_obj){
            return;
        }
        var childs=out_obj.children_node;
        childs.forEach(o => {
        out=out+"\n"+(o.name)+"\n";
    });
    out=out+"\nParent:";
        var parents=out_obj.parent_node;
        parents.forEach(o => {
        out=out+"\n"+(o.name);
    });
    alert(out);

});






addEventListener("keydown", function(event) {
    if (event.keyCode == 89)

        canvas.isDrawingMode=true;
        canvas.freeDrawingBrush.color='red';
        canvas.freeDrawingBrush.width="2";
});



fabric.Canvas.prototype.getItemByName = function(name) {
  var object = null,
      objects = this.getObjects();

  for (var i = 0, len = this.size(); i < len; i++) {
    if (objects[i].name && objects[i].name === name) {
      object = objects[i];
      break;
    }
  }

  return object;
};



function GetActiveNodes(){
    var moni_name=canvas['moni_name']
    var sel_node = canvas.getActiveObject();
    var out_node=moni_name+'/'+sel_node['name']
    return out_node;
}




function NodeUpdate(resp){
        
        canvas.clear();
        let files = resp;

        dir_array=files.dir_arr;
        files_array=Object.keys(files.doit_arr);
        proj_relative_path=files.root;
        in_depth=files.depth;

        canvas['moni_name']=proj_relative_path;
        //createNodes
        files_array.forEach(file_in => {
            coord=files.doit_arr[file_in]['coord'];
            var x=parseFloat(coord[0]);
            var y=parseFloat(coord[1]);
            var nodeA=createNode( file_in , canvas , x , y );
        });

        //createArrows 
        files_array.forEach(file_in => {
            inputs=files.doit_arr[file_in]['inputs'];
            console.log(inputs);
            if (inputs != "None"){
            inputs.forEach(input => {

                nodein=canvas.getItemByName(file_in);
                nodeout=canvas.getItemByName(input);





                if (nodein != null && nodeout != null){
                nodein.parent_node.push(nodeout);
                nodeout.children_node.push(nodein);

                    createArrow(  nodeout , nodein  , canvas , 0 );
                };
            }); 
        };

        });        
   
}




function NodeMonitorSaveGraph(){
    var moni_name=canvas['moni_name']
    console.log("SaveGraphImWork");
    console.log(moni_name);

    request_out={}
    request_body={}
    nodes=canvas.getObjects().filter(obj => obj.type === 'node');
    nodes.forEach(cur_node => {
        console.log(cur_node.name);
        request_body['coord']=[cur_node.left, cur_node.top ];
        let ch_name=[];
        let pr_name=[];
        var ch_arr=cur_node.children_node;
        var pr_arr=cur_node.parent_node;
        console.log(ch_arr);
        console.log(pr_arr);
        console.log(ch_arr.lenght);
        console.log(pr_arr.lenght);
        ch_arr.forEach(ch_node => {
            console.log("AAA");
            console.log(ch_node.name);
            console.log("BBB");
            ch_name.push(ch_node.name);
        });

        pr_arr.forEach(pr_node => {
            console.log("CCC");
            console.log(pr_node.name);
            console.log("DDD");
            pr_name.push(pr_node.name);
        });

        request_body['children_node']=ch_name;
        request_body['parent_node']=pr_name;
        request_out[cur_node.name]=request_body;
    })
    console.log(request_out);

    return nodes;

}


