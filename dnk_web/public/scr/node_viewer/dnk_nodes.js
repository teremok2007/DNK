var Node = fabric.util.createClass(fabric.Circle, {

    type: 'node',

    initialize: function(options) {
    options || (options = { });

    this.callSuper('initialize', options);
    this.set('color_hsl', options.input || []);
    this.set('input', options.input || []);
    this.set('output', options.output || []);
    this.set('children_node', options.children_node || []);
    this.set('parent_node', options.parent_node || []);
    this.set('arrows', options.arrows || []);
    this.set('misk', options.misk || []);
    },

    toObject: function() {
        return fabric.util.object.extend(this.callSuper('toObject'), {
        color_hsl: this.get('color_hsl'),
        input: this.get('input'),
        output: this.get('output'),   
        children_node: this.get('children_node'),
        parent_node: this.get('parent_node'),
        arrows: this.get('arrows'),
        misk: this.get('misk')
        });
    },

    _render: function(ctx) {
    this.callSuper('_render', ctx);

    }
});


var DboxNode = fabric.util.createClass(fabric.Rect, {

    type: 'dbox_node',

    initialize: function(options) {
    options || (options = { });

    this.callSuper('initialize', options);
    this.set('color_hsl', options.input || []);
    this.set('input', options.input || []);
    this.set('output', options.output || []);
    this.set('children_node', options.children_node || []);
    this.set('parent_node', options.parent_node || []);
    this.set('arrows', options.arrows || []);
    this.set('misk', options.misk || []);
    },

    toObject: function() {
        return fabric.util.object.extend(this.callSuper('toObject'), {
        color_hsl: this.get('color_hsl'),
        input: this.get('input'),
        output: this.get('output'),
        children_node: this.get('children_node'),
        parent_node: this.get('parent_node'),
        arrows: this.get('arrows'),
        misk: this.get('misk')
        });
    },

    _render: function(ctx) {
    this.callSuper('_render', ctx);

    }
});



var inputNode = fabric.util.createClass(fabric.Circle, {

    type: 'inputNode',

    initialize: function(options) {
    options || (options = { });

    this.callSuper('initialize', options);
    this.set('parent_node', options.parent_node || []);
    this.set('rest_x', options.rest_x || 0 );
    this.set('rest_y', options.rest_y || 0 );

    },

    toObject: function() {
        return fabric.util.object.extend(this.callSuper('toObject'), {
        parent_node: this.get('parent_node'),
        rest_x: this.get('rest_x'),
        rest_y: this.get('rest_y'),

        });
    },

    _render: function(ctx) {
    this.callSuper('_render', ctx);

    }
});






var outputNode = fabric.util.createClass(fabric.Circle, {

    type: 'outputNode',

    initialize: function(options) {
    options || (options = { });

    this.callSuper('initialize', options);
    this.set('parent_node', options.parent_node || []);
    this.set('rest_x', options.rest_x || 0 );
    this.set('rest_y', options.rest_y || 0 );

    },

    toObject: function() {
        return fabric.util.object.extend(this.callSuper('toObject'), {
        parent_node: this.get('parent_node'),
        rest_x: this.get('rest_x'),
        rest_y: this.get('rest_y'),
        });
    },

    _render: function(ctx) {
    this.callSuper('_render', ctx);

    }
});






var Arrow = fabric.util.createClass(fabric.Line, {

    type: 'arrows',

    initialize: function( points , options) {
    options || (options = { });

    this.callSuper('initialize', points, options);
    this.set('in_node', options.in_node || []);
    this.set('out_node', options.out_node || []);

    },

    toObject: function() {
        return fabric.util.object.extend(this.callSuper('toObject'), {
        in_node: this.get('in_node'),
        out_node: this.get('out_node'),
        });
    },

    _render: function(ctx) {
    this.callSuper('_render', ctx);

    }
});






var Text = fabric.util.createClass(fabric.Text, {

    type: 'name_node',

    initialize: function( points , options) {
    options || (options = { });

    this.callSuper('initialize', points, options);
    this.set('parent_node', options.parent_node || []);
    this.set('name', options.name || 0 );
    this.set('rest_x', options.rest_x || 0 );
    this.set('rest_y', options.rest_y || 0 );
    },

    toObject: function() {
        return fabric.util.object.extend(this.callSuper('toObject'), {
        parent_node: this.get('parent_node'),
        text: this.get('name'),
        rest_x: this.get('rest_x'),
        rest_y: this.get('rest_y'),        
        });
    },

    _render: function(ctx) {
    this.callSuper('_render', ctx);

    }
});







































function createNode(name , canvas , x , y ,override=0 , depth=1 , color_hsl=[194,52,62] ,type_node=0) {

    var h=color_hsl[0];
    var s=color_hsl[1]*depth*depth;
    var l=color_hsl[2]*depth;

    var default_hsl = 'hsl(' + color_hsl[0] + ', ' + (color_hsl[1]) + '%,  ' + (color_hsl[2]) + '%)';
    var node_hsl = 'hsl(' + h + ', ' + s + '%,  ' + l + '%)';

    if(override==0){
        cant_color=default_hsl;

    }
    else{
        cant_color='#FF7D1E';

    }





    
    node_name= String(name);
    nodeRadius=10;
    inoutRadius=3;


    input_name= name + '_in';
    output_name= name + '_out';
    




    if(type_node==0){
        inY=y-nodeRadius-inoutRadius;
        outY=y+nodeRadius+inoutRadius;
        var input = new inputNode({ name: input_name , left: x ,top: inY , radius: inoutRadius , fill: 'white' , hasBorders: false , hasControls: false  });
        var output = new outputNode({ name: output_name , left: x ,top: outY , radius: inoutRadius , fill: 'white' , hasBorders: false , hasControls: false  });
        var node = new Node({name: node_name , left: x ,top: y , radius: nodeRadius , fill: node_hsl , hasBorders: false , stroke : cant_color , strokeWidth : 3 , hasControls: false , zIndex:5  });
    }
    else{
        inY=y;
        outY=y;
        var input = new inputNode({ name: input_name , left: x ,top: inY , radius: inoutRadius , fill: 'white' , hasBorders: false , hasControls: false ,visible: false });
        var output = new outputNode({ name: output_name , left: x ,top: outY , radius: inoutRadius , fill: 'white' , hasBorders: false , hasControls: false, visible: false  });
        var node = new DboxNode({name: node_name , left: x ,top: y , height: 15, width: 15, fill: node_hsl , hasBorders: false , stroke : cant_color , strokeWidth : 3 , hasControls: false ,zIndex:5  });

    }

    var name_text = new Text( node_name , { textAlign: 'left' , left: x ,top: y ,fontSize:15, fill: '#FF7D1E' });
    bound=name_text.getBoundingRect().width;
    name_text.left=name_text.left+bound/2+12;

    node.color_hsl=[h,s,l];
    node.selectable=true;
    input.parent_node = node;
    output.parent_node = node;

    node.input = input;
    node.output = output;




    canvas.add(node,input,output,name_text);


    var multiply = fabric.util.multiplyTransformMatrices;
    var invert = fabric.util.invertTransform;

    let minions = node.misk;
    minions.push(node.input,node.output,name_text);

    var bossTransform = node.calcTransformMatrix();
    var invertedBossTransform = invert(bossTransform);
    minions.forEach(o => {
        var desiredTransform = multiply(
        invertedBossTransform,
        o.calcTransformMatrix()
    );

    o.relationship = desiredTransform;
    });

    input.on('mousedown', updateInDown);
    output.on('mousedown', updateOutDown);
    input.on('mouseup', updateInUp);
    output.on('mouseup', updateOutUp);
    node.on('moving', moveNode);
    node.on('selected', selectNode);
    node.on('deselected', deselectNode);

    node.on('mousedown', (event) => {
    if(event.button === 1) {

    }

    if(event.button === 2) {
        moni_name=canvas['moni_name']
        var sel_node = canvas.getActiveObject();
        data_path=moni_name+'/'+sel_node['name']
        
        var out='Run Select Up Stream : ' +data_path;
        alert(out);
        out_dict={};
        out_dict['path_node']=data_path;
        out_dict['iterator']=[moni_name];
        let select_node = JSON.stringify(out_dict);

        let request = new XMLHttpRequest();
        request.open("POST", "/start_up", true);
        request.setRequestHeader("Content-Type", "application/json");

        request.send(select_node);

        console.log(data_path);


    }
    if(event.button === 3) {






    }
    });


    
    return node;

}


function deleteNode(canvas) {

    var del_node = canvas.getActiveObject();

    if (del_node.type=='node'){


        del_child = del_node.children_node;
        del_parent= del_node.parent_node;
        
        
        del_parent.forEach(del_pc => {
            dpc=del_pc.children_node;
            dpc.splice( dpc.indexOf(del_node), 1 );

        });

        del_child.forEach(del_cp => {
            dcp=del_cp.parent_node;
            dcp.splice( dcp.indexOf(del_node), 1 );
 
        });

        del_input=del_node.input;
        canvas.remove(del_input);
        del_output=del_node.output;
        canvas.remove(del_output);


        del_arrows=del_node.arrows;
        del_arrows.forEach(del_a => {
            canvas.remove(del_a);
        });


        canvas.remove(del_node);

  }

}








function updateInDown() {
    var in_point = canvas.getActiveObject();
    var x=in_point.left;
    var y=in_point.top;
    
    in_point.rest_x=x;
    in_point.rest_y=y;
}


function updateOutDown() {
    var in_point = canvas.getActiveObject();
    var x=in_point.left;
    var y=in_point.top;
    
    in_point.rest_x=x;
    in_point.rest_y=y;
    
}




function updateInUp() {
    var in_point = canvas.getActiveObject();

    out_objects = canvas.getObjects('node');
    
    var x=in_point.left;
    var y=in_point.top;
    
    out_objects.forEach(o => {
        eachX=o.left;
        eachY=o.top;
        subX=Math.abs(eachX-x);
        subY=Math.abs(eachY-y);
        if ((subX < 8) && (subY < 8))
        { 
            nodeOut=o;
            nodeIn=in_point.parent_node;
            
            nodeIn.parent_node.push(nodeOut);
            nodeOut.children_node.push(nodeIn)
            createArrow(nodeOut , nodeIn , canvas , 0 );
        }
    });    


    var restX=in_point.rest_x;
    var restY=in_point.rest_y;
    
    in_point.left=restX;
    in_point.top=restY;
    
    
    


}

function updateOutUp() {
    var out_point = canvas.getActiveObject();
    out_objects = canvas.getObjects('node');


    var x=out_point.left;
    var y=out_point.top;
    
    out_objects.forEach(o => {
        eachX=o.left;
        eachY=o.top;
        subX=Math.abs(eachX-x);
        subY=Math.abs(eachY-y);
        if ((subX < 8) && (subY < 8))
        {
            nodeIn=o;
            nodeOut=out_point.parent_node;
            nodeIn.parent_node.push(nodeOut);
            nodeOut.children_node.push(nodeIn)
            createArrow(nodeOut , nodeIn , canvas , 0 );
        }
    });    





    var restX=out_point.rest_x;
    var restY=out_point.rest_y;

    out_point.left=restX;
    out_point.top=restY;


    

   
}




function moveNode() {

    
    var current_node = canvas.getActiveObject();
    var multiply = fabric.util.multiplyTransformMatrices;
    var invert = fabric.util.invertTransform;

    arrows=current_node.arrows;

    arrows.forEach(arr => {

        updateArrow(arr);
    });



    
    let minions = current_node.misk;
    minions.push(current_node.input , current_node.output );



    minions.forEach(o => {
    if (!o.relationship) {
        return;
    }
    var relationship = o.relationship;
    var newTransform = multiply(
    current_node.calcTransformMatrix(),
    relationship
    );
    opt = fabric.util.qrDecompose(newTransform);
    o.set({
        flipX: false,
        flipY: false,
    });
    o.setPositionByOrigin(
        { x: opt.translateX, y: opt.translateY },
        'center',
        'center'
    );
    o.set(opt);
    o.setCoords();
  });

}



var select_obj_array=[];

function selectNode() {
    
    var current_node = canvas.getActiveObject();
    select_obj_array=current_node;
    current_node.set({fill : 'white'});
    
}


function deselectNode() {

    console.log(select_obj_array);
    var node_color_hsl = 'hsl(' + select_obj_array.color_hsl[0] + ', ' + (select_obj_array.color_hsl[1]) + '%,  ' + (select_obj_array.color_hsl[2]) + '%)';
    select_obj_array.set({fill : node_color_hsl});

    select_obj_array=[];
    
}













function createArrow(nodeOut , nodeIn , canvas , temporary ) {
    if (nodeOut.name == nodeIn.name)
    {
        return;
    }

    fill_arrow="white"
    width_arrow=1
    node_in=nodeIn.input;
    node_out=nodeOut.output;
    sel=true;

    if(temporary==0){
        
        nodeInRadius=nodeIn.radius;
        nodeOutRadius=nodeOut.radius;
        inoutRadius=node_in.radius;
    }
    else{
        fill_arrow="#05FA15"
        if(temporary==2){
            fill_arrow="#E01700"
        }
        width_arrow=0.5
        nodeInRadius=0
        nodeOutRadius=0
        inoutRadius=0;
        sel=false;
    }
    

    

    
    var x1=nodeIn.left;
    var y1=nodeIn.top-nodeInRadius-inoutRadius;
    
    var x2=nodeOut.left;
    var y2=nodeOut.top+nodeOutRadius+inoutRadius;

    top=(y1+y2)/2;
    left=(x1+x2)/2;
    var arrow_points= [ x1, y1, x2, y2 ];
    var arrow_name=nodeIn.name+'_'+nodeOut.name;

    var arrow = new Arrow( arrow_points , { name: arrow_name , strokeWidth: width_arrow , fill: fill_arrow, stroke: fill_arrow, originX: 'center', originY: 'center', hasBorders: false , hasControls: false , selectable : sel ,lockMovementX: true , lockMovementY: true, targetFindTolerance: 8 });
    arrow.in_node=nodeIn;
    arrow.out_node=nodeOut;
    
    
    
    nodeOut.arrows.push(arrow);
    nodeIn.arrows.push(arrow);
    arrow.set({ 'top': top, 'left': left, 'x1': x1, 'y1': y1 , 'x2': x2, 'y2': y2 });
    canvas.add(arrow);


    arrow.on('selected', selectArrow);
    arrow.on('deselected', deselectArrow);
    
    return arrow;

    
}




function updateArrow(in_arrow) {
    nodeIn=in_arrow.in_node;
    nodeOut=in_arrow.out_node;
    node_in=nodeIn.input;
    node_out=nodeOut.output;
    
    var x1=node_in.left;
    var y1=node_in.top;
    var x2=node_out.left;
    var y2=node_out.top;
    if (nodeIn.type=='dbox_node'){
        //Centered by node
        var x2=nodeOut.left;
        var y2=nodeOut.top;
    }

    var coord=x1+'_'+y1+'_'+x2+'_'+y2;

    var arrow_points= [ x1, y1, x2, y2 ];
    in_arrow.set({ 'x1': x1, 'y1': y1 , 'x2': x2, 'y2': y2 });
    
    
}


var select_arrow_array=[];

function selectArrow() {

    var current_node = canvas.getActiveObject();
    select_arrow_array.push(current_node);
    current_node.set({stroke: 'yellow'});
    
}

function deselectArrow() {
    if (select_arrow_array.length !=0)
    {   
        select_arrow_array.forEach(arr_obj => {
        arr_obj.set({stroke: 'white'});
        });
        select_arrow_array=[];
    }
}






function deleteArrow(arr_remove) {

        input_node = arr_remove.in_node;
        out_node = arr_remove.out_node;

        console.log('pre_children_node');
        console.log(input_node.name,out_node.name);


        del_child = out_node.children_node;
        del_parent= input_node.parent_node;

        console.log(del_child.length,del_parent.length);

        for (i=0 ; i<del_child.length ; i++){
            console.log( out_node.name ,':childs-' ,del_child[i].name);
            if (del_child[i].name==input_node.name){
                console.log('REMOVE',del_child[i].name );
                del_child.splice( i,1 );
            }
        }
        for (i=0;i<del_parent.length;i++){
            console.log(input_node.name,':parents-', del_parent[i].name);
            if (del_parent[i].name==out_node.name){
                console.log('REMOVE',del_parent[i].name );
                del_parent.splice( i,1 );
            }
        }
        out_node['children_node']=del_child;
        input_node['parent_node']=del_parent;

        console.log(out_node['children_node']);
        console.log(input_node['parent_node']);

        in_arrows=input_node.arrows;
        out_arrows=out_node.arrows;

        input_node.arrows = in_arrows.splice( in_arrows.indexOf(arr_remove) );
        out_node.arrows = out_arrows.splice( out_arrows.indexOf(arr_remove) );

    canvas.remove(arr_remove);
    
}









