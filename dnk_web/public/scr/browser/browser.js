$(document).ready(function()
{



        project_name="";
        folder_depth=0;

        let get_files = JSON.stringify({directory: project_name , parent_name: "file_browser" ,depth_folder:folder_depth});

        let request = new XMLHttpRequest();
        request.open("POST", "/get_files", true);
        request.setRequestHeader("Content-Type", "application/json");

        request.addEventListener("load", function () {

            let files = JSON.parse(request.response);
            var node = document.getElementById(files.parent);
            dir_array=files.dir_arr;
            files_array=files.files_arr;
            proj_relative_path=files.root;
            in_depth=files.depth;
            dir_array.forEach(dir_in => {
                let dir = document.createElement('div');

                dir.className = "bwr_folder";
                dir.id=proj_relative_path+"/"+dir_in;
                dir.dataset.open=0;
                dir.dataset.depth=in_depth;
                dir.innerHTML = "<div> <div class=\"space\" style=\"padding-left:"+in_depth+"px\"><\div> <img src=\"/public/icons/folder/keyboard_arrow_right-12px.svg\"> <img src=\"/public/icons/folder/folder-12px.svg\"> " + dir_in +"</div>";
                node.append(dir);

                let dir_box = document.createElement('div');
                dir_box.className = "bwr_folder_box";
                dir_box.id=proj_relative_path+"/"+dir_in+"_box";
                dir_box.dataset.open=0;
                node.append(dir_box);

                dir.addEventListener("dblclick",function (e){

                  new_path=this.id;
                  parent_path=this.id+"_box";


                  if(this.dataset.open==1)
                  {
                      this.dataset.open=0;
                      var folder_box = document.getElementById(parent_path);
                      folder_box.innerHTML = '';
                      this.innerHTML = "";
                      this.innerHTML = "<div> <div class=\"space\" style=\"padding-left:"+this.dataset.depth+"px\"><\div> <img src=\"/public/icons/folder/keyboard_arrow_right-12px.svg\"> <img src=\"/public/icons/folder/folder-12px.svg\"> " + dir_in +"</div>";

                      return 1;
                  }
                  else if (this.dataset.open==0) {
                      this.dataset.open=1;
                  }
                  this.innerHTML = "";
                  this.innerHTML = "<div> <div class=\"space\" style=\"padding-left:"+this.dataset.depth+"px\"><\div> <img src=\"/public/icons/folder/keyboard_arrow_down-12px.svg\"> <img src=\"/public/icons/folder/folder-12px.svg\"> " + dir_in +"</div>";
                  folder_depth=parseInt(this.dataset.depth)+12;
                  let get_dir = JSON.stringify({directory: new_path , parent_name :parent_path ,depth_folder:folder_depth});

                  request.open("POST", "/get_files", true);
                  request.setRequestHeader("Content-Type", "application/json");
                  request.send(get_dir);
                  //alert(new_path);
                 });

              });
            files_array.forEach(file_in => {
                let file = document.createElement('div');
                file.className = "file";
                file.dataset.id = file_in;
                file.innerHTML = "<div> <div class=\"space\" style=\"padding-left:"+in_depth+"px\"><\div> " + file_in +"</div>";
                node.append(file);
            });

        });


        request.send(get_files);








        "use strict";




        function clickInsideElement( e, className ) {
            var el = e.srcElement || e.target;

            if ( el.classList.contains(className) ) {
                return el;
            } else {
                while ( el = el.parentNode ) {
                    if ( el.classList && el.classList.contains(className) ) {
                        return el;
                    }
                }
            }

            return false;
        }



        function getPosition(e) {
            var posx = 0;
            var posy = 0;

            if (!e) var e = window.event;

            if (e.pageX || e.pageY) {
                posx = e.pageX;
                posy = e.pageY;
            } else if (e.clientX || e.clientY) {
                posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
                posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
            }

            return {
                x: posx,
                y: posy
            }
        }


        /**
           * Variables.
           */
           var contextMenuClassName = "context-menu";
           var contextMenuItemClassName = "context-menu__item";
           var contextMenuLinkClassName = "context-menu__link";
           var contextMenuActive = "context-menu--active";

           var taskItemClassName = "file";
           var taskItemInContext;

           var clickCoords;
           var clickCoordsX;
           var clickCoordsY;

           var menu = document.querySelector("#context-menu");
           var menuItems = menu.querySelectorAll(".context-menu__item");
           var menuState = 0;
           var menuWidth;
           var menuHeight;
           var menuPosition;
           var menuPositionX;
           var menuPositionY;

           var windowWidth;
           var windowHeight;

          /**
           * Initialise our application's code.
           */
           function init() {
               contextListener();
               clickListener();
               keyupListener();
               resizeListener();
           }



           /**
            * Listens for contextmenu events.
            */
           function contextListener() {
             document.addEventListener( "contextmenu", function(e) {
               taskItemInContext = clickInsideElement( e, taskItemClassName );

               if ( taskItemInContext ) {
                 e.preventDefault();
                 toggleMenuOn();
                 positionMenu(e);
               } else {
                 taskItemInContext = null;
                 toggleMenuOff();
               }
             });
           }

           /**
            * Listens for click events.
            */
           function clickListener() {
             document.addEventListener( "click", function(e) {
               var clickeElIsLink = clickInsideElement( e, contextMenuLinkClassName );

               if ( clickeElIsLink ) {
                 e.preventDefault();
                 menuItemListener( clickeElIsLink );
               } else {
                 var button = e.which || e.button;
                 if ( button === 1 ) {
                   toggleMenuOff();
                 }
               }
             });
           }

           /**
            * Listens for keyup events.
            */
           function keyupListener() {
             window.onkeyup = function(e) {
               if ( e.keyCode === 27 ) {
                 toggleMenuOff();
               }
             }
           }

           /**
            * Window resize event listener
            */
           function resizeListener() {
             window.onresize = function(e) {
               toggleMenuOff();
             };
           }

           /**
            * Turns the custom context menu on.
            */
           function toggleMenuOn() {
             if ( menuState !== 1 ) {
               menuState = 1;
               menu.classList.add( contextMenuActive );
             }
           }

           /**
            * Turns the custom context menu off.
            */
           function toggleMenuOff() {
             if ( menuState !== 0 ) {
               menuState = 0;
               menu.classList.remove( contextMenuActive );
             }
           }

           /**
            * Positions the menu properly.
            *
            * @param {Object} e The event
            */
           function positionMenu(e) {
             clickCoords = getPosition(e);
             clickCoordsX = clickCoords.x;
             clickCoordsY = clickCoords.y;

             menuWidth = menu.offsetWidth + 4;
             menuHeight = menu.offsetHeight + 4;

             windowWidth = window.innerWidth;
             windowHeight = window.innerHeight;

             if ( (windowWidth - clickCoordsX) < menuWidth ) {
               menu.style.left = windowWidth - menuWidth + "px";
             } else {
               menu.style.left = clickCoordsX + "px";
             }

             if ( (windowHeight - clickCoordsY) < menuHeight ) {
               menu.style.top = windowHeight - menuHeight + "px";
             } else {
               menu.style.top = clickCoordsY + "px";
             }
           }

           /**
            * Dummy action function that logs an action when a menu item link is clicked
            *
            * @param {HTMLElement} link The link that was clicked
            */
           function menuItemListener( link ) {
             console.log( "Task ID - " + taskItemInContext.getAttribute("data-id") + ", Task action - " + link.getAttribute("data-action"));
             toggleMenuOff();
           }

           /**
            * Run the app.
            */
           init();
























});
