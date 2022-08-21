
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



function SelectEventsOnChange(theSelect){
    // mudar  o video 
    /*
    // The new image to display
    var districtImageFile = "images/distritos/" + selectedClass + ".gif";
    document.getElementById("imgDistrict").src = districtImageFile;
    */
    
    // The new option
    var selectedClass = theSelect.value;

    var args = "class="+selectedClass;
    
    //alert(selectedClass);
    // With HTTP GET method
    xmlHttp = GetXmlHttpObject();
    xmlHttp.open("GET", "get.php?" + args, true);
    xmlHttp.onreadystatechange=SelectEventsHandleReply;
    xmlHttp.send(null);
    
    
}

function SelectEventsHandleReply(){
    //alert( xmlHttp.readyState );
  
  if( xmlHttp.readyState === 4 && xmlHttp.status === 200) {
    var countySelect=document.getElementById("county");

    countySelect.options.length = 0;
    var counties = JSON.parse( xmlHttp.responseText );
    
    //alert( counties );
    
    for (i=0; i<counties.length; i++) {
      var currentCounty = counties[i];
      
      var value  = currentCounty.index;
      var option = currentCounty.type;
	  
      try{
        countySelect.add( new Option("", value), null);
      }
      catch(e) {
        countySelect.add( new Option("", value) );
      }
      
      countySelect.options[i].innerHTML = option;
    }
  }
}







// The District Select has change
function SelectDistrictChange(theSelect) {
  // The new option
  var selectedDistrict = theSelect.value;
  
  // The new image to display
  var districtImageFile = "images/distritos/" + selectedDistrict + ".gif";
  document.getElementById("imgDistrict").src = districtImageFile;

  // Preparing the arguments to request the counties
  var args = "district="+selectedDistrict;
  
  // With HTTP GET method
  xmlHttp = GetXmlHttpObject();
  xmlHttp.open("GET", "getCounties.php?"+args, true);
  xmlHttp.onreadystatechange=SelectDistrictHandleReply;
  xmlHttp.send(null);
}

//Fill in the counties for the new district
function SelectDistrictHandleReply() {
  
  //alert( xmlHttp.readyState );
  
  if( xmlHttp.readyState === 4 ) {
    var countySelect=document.getElementById("county");

    countySelect.options.length = 0;

    //alert( xmlHttp.responseText );
    
    var counties = JSON.parse( xmlHttp.responseText );
    
    //alert( counties );

    for (i=0; i<counties.length; i++) {
      var currentCounty = counties[i];
      
      var value  = currentCounty.idCounty;
      var option = currentCounty.nameCounty;
	  
      try{
        countySelect.add( new Option("", value), null);
      }
      catch(e) {
        countySelect.add( new Option("", value) );
      }
      
      countySelect.options[i].innerHTML = option;
    }
  }
}

