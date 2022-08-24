<?php

include_once 'Lib/lib.php';
include_once './Lib/constants.php';




if(isset($_GET['currentClipNumber'])){
    $number = $_GET[ "currentClipNumber" ];
}
if(isset($_GET['next'])){
    $next = $_GET[ "next" ];
}
if(isset($_GET['event'])){
    $event = $_GET[ "event" ];
}


if($event == "all"){
    $result = getAllEventTypeClipInfo($directoryVideoPath, $next, $number);
}
else if ($event == "noise" || $event == "ball-hit"){
    $result = getEventTypeClipInfo($directoryVideoPath, $next, $number, $event);
}
else{
    echo "Invalid data!"; exit(0);
}




echo json_encode($result);

