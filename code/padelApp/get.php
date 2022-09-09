<?php

include_once 'Lib/lib.php';
include_once './Lib/constants.php';

if(isset($_GET['class'])){
    $class = $_GET[ "class" ];
}

if(isset($_GET['sorted'])){
    $sorted = $_GET[ "sorted" ];
}


//$class= "all";
//$sorted = "true";

if ( !isset($_SESSION) ) {
    session_start();
}

$directoryVideoPath = "videos/" . $_SESSION["video_name"];


if($sorted == 'true') {$clips_info_file_name = $clips_info_sorted;}
else {$clips_info_file_name = $clips_info_non_sorted;}

$result = get($directoryVideoPath, $clips_info_file_name, $sorted, desiredType: $class);

//echo json_encode($result);
echo json_encode($result);

