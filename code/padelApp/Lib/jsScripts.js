
var xmlHttp;

function GetXmlHttpObject() {
  try {
    return new ActiveXObject("Msxml2.XMLHTTP");
  } catch(e) {} // Internet Explorer
  try {
    return new ActiveXObject("Microsoft.XMLHTTP");
  } catch(e) {} // Internet Explorer
  try {
    return new XMLHttpRequest();
  } catch(e) {} // Firefox, Opera 8.0+, Safari
  alert("XMLHttpRequest not supported");
  return null;
}


var selectedClass;
function SelectEventsOnChange(theSelect){
    // mudar  o video 
    /*
    // The new image to display
    var districtImageFile = "images/distritos/" + selectedClass + ".gif";
    document.getElementById("imgDistrict").src = districtImageFile;
    */
    
    // The new option
    selectedClass = theSelect.value;

    var args = "class="+selectedClass;
    
    //alert(selectedClass);
    // With HTTP GET method
    xmlHttp = GetXmlHttpObject();
    xmlHttp.open("GET", "get.php?" + args, true);
    xmlHttp.onreadystatechange=SelectEventsHandleReply;
    xmlHttp.send(null);
    
    
}

function SelectEventsHandleReply(){
  
  if( xmlHttp.readyState === 4 ) {
    //alert( xmlHttp.responseText );
    
    var clips = JSON.parse( xmlHttp.responseText );
    
    // eliminar os elementos filhos no container
    var container = document.getElementById("selectsContainer");
    container.innerHTML  = '';
    
    // para cada video
    for (i=0; i < clips.length; i++) {
        
        var currentClip = clips[i];
        var option = currentClip.type;
        var value  = currentClip.index;
        var name  = currentClip.name;
       
        // criar um select
        var newSelect = document.createElement("SELECT");
        newSelect.setAttribute("id", "select" + value);
        
        // colocar as options dentro do select
        insertOptions(newSelect, value, option);
                
        // adicionar o select ao contentor
        container.appendChild(newSelect);
        
        // colocar botão de play
        var playbttn = document.createElement("BUTTON");
        var text = document.createTextNode("Click me");
        playbttn.appendChild(text);
        playbttn.type="button";
        playbttn.onclick = LoadVideo(name);
        container.appendChild(playbttn);
        
        // criar <br>
        var br = document.createElement("BR");
        container.appendChild(br);
        var br = document.createElement("BR");
        container.appendChild(br);
        
    }
  }
}

function LoadVideo(name){
    // mudar o source do video
    document.getElementById("vid").src = "videos/vid_20_08_2022_17_22/clips" + name;
}


function insertOptions(selectElement, value, option){
    var newValue = option + "_" +value;
    try{
      selectElement.add( new Option(option, newValue), null);
    }
    catch(e) {
      selectElement.add( new Option(option, newValue) );
    }

    selectElement.options[0].innerHTML = option;
    
    if(option === "noise"){
        option = "ball-hit";
        var newValue = option + "_" +value;
        
        try{
            selectElement.add( new Option(option, newValue), null);
          }
          catch(e) {
            selectElement.add( new Option(option, newValue) );
          }

          selectElement.options[1].innerHTML = option;
    }
    
    else if(option === "ball-hit"){
        option = "noise";
        var newValue = option + "_" +value;
        
        try{
            selectElement.add( new Option(option, newValue), null);
          }
          catch(e) {
            selectElement.add( new Option(option, newValue) );
          }

          selectElement.options[1].innerHTML = option;
    }
}


function SelectAllEvents(){
   
    // The new option
    selectedClass = "all";

    var args = "class="+selectedClass;
    
    //alert(selectedClass);
    // With HTTP GET method
    xmlHttp = GetXmlHttpObject();
    xmlHttp.open("GET", "get.php?" + args, true);
    xmlHttp.onreadystatechange=SelectEventsHandleReply;
    xmlHttp.send(null);
}

function LoadClasses(classesArray){
    
    
    var selectElement = document.getElementById("classSelect");
    for (let i = 0; i < classesArray.length; i++) {
        var optionName = classesArray[i];
        var value = optionName;
        
        try{
            selectElement.add( new Option(optionName, value), null);
        }
        catch(e) {
          selectElement.add( new Option(optionName, value));
        }
        
        // i+1 por causa da opção "all" que já lá está
        selectElement.options[i+1].innerHTML = optionName; 
    }
}