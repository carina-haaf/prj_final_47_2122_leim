<?php

include_once 'Lib/lib.php';

$directory_path = "videos/vid_20_08_2022_17_22/hits";
$class = $_GET[ "class" ];

$result = getVideoNamesByClass($directory_path);


/*
$result = array();
$result[] = array( 
            'idCounty'=>-1, 
            'nameCounty'=>$class );
 * 
 */

echo json_encode($result);
?>


<?php
