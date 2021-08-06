function iterator_update(nav_path) {

    return 1;

};










var myIterFolders=[];


function iterator_add_selection(select_id) {
    console.log(select_id);
    myIterFolders.push(select_id);
    var sel_fldr = document.getElementById(select_id);
    sel_fldr.style.backgroundColor ="#eaeaea";
    console.log(myIterFolders) 
};



function iterator_clear_selection() {
    myIterFolders.forEach(folder_id => {
        var sel_fldr = document.getElementById(folder_id);
        sel_fldr.style.backgroundColor ="#C7E495";
    });
    myIterFolders=[];
    console.log(myIterFolders);
};




function iterator_add_shift_selection(select_id) {
    var all_fldr = document.getElementById('iterator').children;
    if (myIterFolders.length==0){
        myIterFolders.push(select_id);
    }

    var sel_fldr = document.getElementById(select_id);
    sel_fldr.style.backgroundColor ="#eaeaea";

    arr_tmp_in=[];
    arr_tmp=[];
    if (myIterFolders.length>0){
        arr_tmp_in.push(parseInt(document.getElementById(myIterFolders[myIterFolders.length-1]).dataset.n));
        arr_tmp_in.push(parseInt(document.getElementById(select_id).dataset.n));
        arr_tmp=arr_tmp_in.sort((a, b) => a - b);

    for (var it in all_fldr){

        if (all_fldr[it].className=='iterator_folder'){


            current_n=parseInt(all_fldr[it].dataset.n);
            if (current_n >= arr_tmp[0] && current_n <= arr_tmp[1]){
                myIterFolders.push(all_fldr[it].id);
                all_fldr[it].style.backgroundColor ="#eaeaea";
            }
        }

        
    }
}
    var names = myIterFolders;
    var uniqueNames = [];
    $.each(names, function(i, el){
    if($.inArray(el, uniqueNames) === -1) uniqueNames.push(el);
    });
    myIterFolders=uniqueNames
    console.log(myIterFolders);

};




