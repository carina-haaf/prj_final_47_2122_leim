<?php

include_once 'Lib/lib.php';
include_once './Lib/constants.php';

if(isset($_GET['class'])){
    $class = $_GET[ "class" ];
}


$result = get($directoryVideoPath, desiredType: $class);

echo json_encode($result);

