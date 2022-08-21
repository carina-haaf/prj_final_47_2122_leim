<?php


function getDirNumberOfFiles($directory){
    
    $files = scandir($directory);    

    return count($files) - 2;
}


function getClassesName($directory_path){
    
    $files = scandir($directory_path);
    $classes = array();
    for($i = 0; $i < getDirNumberOfFiles($directory_path); $i++){
        $str = $files[$i];
        $str2 = explode(".", $str )[0];
        $str3 = explode("_", $str2 )[2];
        
        $class = $str3;
        $classes[] = $class;
    }    
    return $classes;
}


function getVideoNamesByClass($directory_path){
    
    $files = scandir($directory_path);


    for($x = 2; $x < count($files) - 2; $x++) {

        $videoNumber = getVideoNumber($files[$x]);
        $video_class = getVideoClass($files[$x]);

        
        $result[] = array( 
            'index'=>$videoNumber, 
            'type'=> $video_class);
    }
    
    return $result;
}


function getVideoClass($videoName){
    $str = $videoName;
    $str2 = explode(".", $str )[0];
    $str3 = explode("_", $str2 )[2];

    $class = $str3;
    
    return $class;
}

function getVideoNumber($videoName){
    $str = $videoName;
    $str2 = explode(".", $str )[0];
    $str3 = explode("_", $str2 )[1];

    $number = $str3;
    
    return $number;
}








