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
if(isset($_GET['sorted'])){
    $sorted = $_GET[ "sorted" ];
}


if ( !isset($_SESSION) ) {
    session_start();
}

$directoryVideoPath = "videos/" . $_SESSION["video_name"];


if($sorted == 'true') {$clips_info_file_name = $clips_info_sorted;}
else {$clips_info_file_name = $clips_info_non_sorted;}

if($event == "all"){
    $result = getAllEventTypeClipInfo($directoryVideoPath, $next, $number, $clips_info_file_name, $sorted);
    
    
}
else if ($event == "noise" || $event == "ball-hit"){
    $clips_info_file_name = $clips_info_non_sorted;
    $result = getEventTypeClipInfo($directoryVideoPath, $next, $number, $clips_info_file_name, $event);
}
else{
    echo "Invalid data!"; exit(0);
}

echo json_encode($result);



