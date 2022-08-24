
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
var dirVideoPath;
function SelectEventsOnChange(theSelect, dirVidpath){
      
    // The new option
    selectedClass = theSelect.value;
    dirVideoPath = dirVidpath;
    
    
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
            var ini = currentClip.ini;
            var fin = currentClip.fin;

            // criar um select com o tipo de evento
            var newSelect = document.createElement("SELECT");
            newSelect.setAttribute("id", "select" + value);

            // colocar as options dentro do select
            insertOptions(newSelect, value, option);

            // colocar botão de SelectEvent
            var playbttn = document.createElement("BUTTON");
            var text = document.createTextNode("Select Event");
            playbttn.appendChild(text);
            playbttn.type="button";
            playbttn.id = value;
            playbttn.setAttribute("name", "play");
            playbttn.setAttribute("class", name);

            var onclickEvent = " SetEventPeriod('" + ini + "', '" + fin + "');";
            onclickEvent += "LoadNewVideo('" + name.trim() + "');";
            playbttn.setAttribute("onclick", onclickEvent);

            // colocar <br>
            var br1 = document.createElement("BR");
            var br2 = document.createElement("BR");

            // colocar tempos inicial e final
            var iniTextNode = document.createTextNode(ini); 
            var finTextNode = document.createTextNode(fin); 

            // adicionar ao contentor/div
            container.appendChild(newSelect);
            container.appendChild(playbttn);
            container.appendChild(iniTextNode);
            container.appendChild(finTextNode);

            container.appendChild(br1);
            container.appendChild(br2);
        }
        
        // garantir que quando o refresh é feito, o primeiro vídeo 
        // selecionado e o período correpondente estão em concordância
        if (clips.length !== 0) {
            var currentClip = clips[0];
            var name  = currentClip.name;
            var ini = currentClip.ini;
            var fin = currentClip.fin;

            SetEventPeriod(ini, fin); 
            LoadNewVideo(name);
        }
    }
}

function SetEventPeriod(ini, fin){
    
    var container = document.getElementById("videoDiv");
    container.innerHTML = '';
    
    var p = document.createElement("P");
    var str = "Selected period: " + ini + " - " + fin;
    const text = document.createTextNode(str);
    
    p.appendChild(text);
    container.appendChild(p);
    
}

function LoadNewVideo(clipName){
    
    LoadVideo(dirVideoPath, clipName);
}


function LoadVideo(directoryVideoPath, clipName){
    
    var container = document.getElementById("videoDiv");
    
    var video = document.createElement('VIDEO');
    var source = document.createElement('SOURCE');
    
    var clipNumber = clipName.split("_")[1];
    
    
    video.setAttribute("id", "video");
    video.setAttribute("class", "video");
    video.setAttribute("width", "100");
    video.setAttribute("controls", '');
    video.setAttribute("name", clipNumber);
    
    var path = directoryVideoPath + '/clips/' + clipName;
    source.setAttribute('src', path);
    source.setAttribute('type', 'video/mp4');
    
    video.appendChild(source);
    container.appendChild(video);    
    
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


function SelectAllEvents(directoryVideoPath){
    
    dirVideoPath = directoryVideoPath;
   
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


function GetNextClip(directoryVideoPath, number){
    
    dirVideoPath = directoryVideoPath;
    
    var eventType = document.getElementById("classSelect").value;
    var args = "currentClipNumber="+number+"&next=true&event="+eventType;
    
    xmlHttp = GetXmlHttpObject();
    xmlHttp.open("GET", "nextPrevious.php?" + args, true);
    xmlHttp.onreadystatechange=GetNextpreviousClipHandleReply;
    xmlHttp.send(null);
}

function GetPreviousClip(directoryVideoPath, number){
    dirVideoPath = directoryVideoPath;
    
    var eventType = document.getElementById("classSelect").value;
    var args = "currentClipNumber="+number+"&next=false&event="+eventType;
    
    xmlHttp = GetXmlHttpObject();
    xmlHttp.open("GET", "nextPrevious.php?" + args, true);
    xmlHttp.onreadystatechange=GetNextpreviousClipHandleReply;
    xmlHttp.send(null);
}

function GetNextpreviousClipHandleReply(){
    
    if( xmlHttp.readyState === 4 ) {
    
        var clips = JSON.parse( xmlHttp.responseText );

        if (clips.length !== 0) {
            var currentClip = clips[0];
            var name  = currentClip.name;
            var ini = currentClip.ini;
            var fin = currentClip.fin;

            SetEventPeriod(ini, fin); 
            LoadNewVideo(name);
        }
        
        else{
            alert("You reached the limit.");
        }
    }
}

