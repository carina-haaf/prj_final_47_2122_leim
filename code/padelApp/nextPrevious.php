<?php

include_once 'Lib/lib.php';
include_once './Lib/constants.php';

if(isset($_GET['currentClipNumber'])){
    $number = $_GET[ "currentClipNumber" ];
}

if(isset($_GET['next'])){
    $next = $_GET[ "next" ];
}

$result = getClipInfo($directoryVideoPath, $next, $number);


echo json_encode($result);

