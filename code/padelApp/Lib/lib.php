<?php

function getVideoDirNames($videoDirPath){
    $files = scandir($videoDirPath);    
    
    for($i = 0; $i < count($files); $i++){
        if($files[$i] !== "." && $files[$i] !== ".."){
            $array[] = $files[$i];
        }
    }
    return $array;
    
}



function getDirNumberOfFiles($directory){
    
    $files = scandir($directory);    

    return count($files) - 2;
}


function get($directoryVideoPath, $clips_info_file_name, $sorted, $desiredType="all"){
    $result = array();
   
    // abrir o ficheiro
    $pathToDataClassesFile = $directoryVideoPath . "/" . $clips_info_file_name;
    $myfile = fopen($pathToDataClassesFile, "r") or die("Unable to open file!");
    
    //iterar sobre o ficheiro
    while(!feof($myfile)) {
        $line = fgets($myfile);

        // colocar no array: indice, t_ini, t_fin, nome do mini clip
        // mas antes garantir que estes valores existem
        $info = explode(";", $line );
        if(isset($info[0]) && isset($info[3]) && isset($info[4]) && 
                isset($info[5]) && isset($info[6]) && isset($info[0]) && 
                isset($info[1]) && isset($info[7])){
            $index = $info[0];
            $ini_idx = $info[1];
            $fin_idx = $info[2];
            $type = $info[5];
            $ini = $info[3];
            $fin = $info[4];
            $name = $info[6];
            $prob = $info[7];
        }
        
        // caso se queira só os clips de uma classe não vale a pena
        // colocar os exemplos de outras classes também
        if( ($type !== $desiredType && $desiredType !== "all")){continue;}
                
        $result[] = array(
            'index'=>$index, 
            'type'=> $type,
            'ini' => $ini,
            'fin' => $fin,
            'ini_idx' => $ini_idx,
            'fin_idx' => $fin_idx,
            'name' => $name,
            'prob' => $prob);
    }
    fclose($myfile);
    
    if($result && $sorted === 'true'){ sort($result); }
    
    return $result;
    
}


function getDataClasses($directoryVideoPath){
    
    $pathToDataClassesFile = $directoryVideoPath . "/dataset/dataset_classes.txt";
    $myfile = fopen($pathToDataClassesFile, "r") or die("Unable to open file!");
    
    while(!feof($myfile)) {
      $line = fgets($myfile);
    }
    fclose($myfile);
    $classeNames = explode(";", $line );
    
    return $classeNames;
}
   

function getFirstClipName($directoryVideoPath, $clips_info_file_name){
    // abrir o ficheiro
    $pathToDataClassesFile = $directoryVideoPath . "/" . $clips_info_file_name;
    $myfile = fopen($pathToDataClassesFile, "r") or die("Unable to open file!");
    
    $line = fgets($myfile);
    $info = explode(";", $line );
    
    if(isset($info[6])){
        $name = $info[6];
    }
    
    return $name;
}

function getFirstClipIniAndFin($directoryVideoPath, $clips_info_file_name){
   
    $pathToDataClassesFile = $directoryVideoPath . "/". $clips_info_file_name;
    $myfile = fopen($pathToDataClassesFile, "r") or die("Unable to open file!");
    
    $line = fgets($myfile);
    $info = explode(";", $line );
    
    if(isset($info[3]) && isset($info[4])){
        $ini = $info[3];
        $fin = $info[4];
    }
    
    return array($ini, $fin);
}


function getAllEventTypeClipInfo($directoryVideoPath, $next, $number, $clips_info_file_name, $sorted){
    if($sorted == 'true'){
        $desiredClipNumber = getClipIndexByNumber($directoryVideoPath, $clips_info_file_name, $number);
        if($next == 'true') { $desiredClipNumber += 1; }
        else if($next == 'false') { $desiredClipNumber -= 1; } 
        
    }
    
    else{
        if($next == 'true') { $desiredClipNumber = 0 +$number + 1; }
        else if($next == 'false') { $desiredClipNumber = 0 +$number - 1; } 
        else { echo 'Invalid $next value!'; exit(0); }
      
    }
    
       
    $pathToDataClassesFile = $directoryVideoPath . "/". $clips_info_file_name;
    $myfile = fopen($pathToDataClassesFile, "r") or die("Unable to open file!");
    
    while(!feof($myfile)) {
        $line = fgets($myfile);

        $info = explode(";", $line );
        if(isset($info[0]) && isset($info[3]) && isset($info[4]) && 
                isset($info[5]) && isset($info[6]) && isset($info[0]) && 
                isset($info[1])){
            $index = $info[0];
            $ini_idx = $info[1];
            $fin_idx = $info[2];
            $type = $info[5];
            $ini = $info[3];
            $fin = $info[4];
            $name = $info[6];
        }
        
        //echo $index ."  ".$desiredClipNumber. "<br>";
        if( $index == $desiredClipNumber){
            $result[] = array(
            'index'=>$index, 
            'type'=> $type,
            'ini' => $ini,
            'fin' => $fin,
            'ini_idx' => $ini_idx,
            'fin_idx' => $fin_idx,
            'name' => $name);
        
        fclose($myfile);
        return $result;
        }
        
        
    }
    fclose($myfile);
    
    return array();
}

function getClipIndexByNumber($directoryVideoPath, $clips_info_file_name, $number){
    $pathToDataClassesFile = $directoryVideoPath . "/". $clips_info_file_name;
    $myfile = fopen($pathToDataClassesFile, "r") or die("Unable to open file!");
       
    
    while(!feof($myfile)) {
        $line = fgets($myfile);

        $info = explode(";", $line );
        if(isset($info[0])&& isset($info[6])){
            $index = $info[0];
            $name = $info[6];
             
            $current_clip_nr = explode("_", $name )[1];
            if($current_clip_nr == $number){
                fclose($myfile);
                return $index;
            }
            
        } 
    }
    
    fclose($myfile);
    return -1;
}


function getEventTypeClipInfo($directoryVideoPath, $next, $number, $clips_info_file_name, $desiredType="all"){ 
    $pathToDataClassesFile = $directoryVideoPath . "/" . $clips_info_file_name;
    
    $myfile = fopen($pathToDataClassesFile, "r") or die("Unable to open file!");
    $result = array();
    
    while(!feof($myfile)) {
        $line = fgets($myfile);

        $info = explode(";", $line );
        if(isset($info[0]) && isset($info[3]) && isset($info[4]) && 
                isset($info[5]) && isset($info[6])){
            $index = $info[0];
            $ini_idx = $info[1];
            $fin_idx = $info[2];
            $type = $info[5];
            $ini = $info[3];
            $fin = $info[4];
            $name = $info[6];
        }
        
        if($type !== $desiredType && $desiredType !== "all"){continue;}
        
        if($next === "true" && 0+$index > 0+$number){
            $result[] = array(
                'index'=>$index, 
                'type'=> $type,
                'ini' => $ini,
                'fin' => $fin,
                'ini_idx' => $ini_idx,
                'fin_idx' => $fin_idx,
                'name' => $name);

            fclose($myfile);
            return $result;
        }
        
        
        if($next === "false" && $index < $number){
            $result[] = array(
                'index'=>$index, 
                'type'=> $type,
                'ini' => $ini,
                'fin' => $fin,
                'ini_idx' => $ini_idx,
                'fin_idx' => $fin_idx,
                'name' => $name);
        }
    }
    
    if($next == "false" && count($result) > 0){
        fclose($myfile);
        $size = count($result);
        $result[] = $result[$size - 1];
        return $result;
    }
    
    return array();
}


function getNumberOfExamples($directoryVideoPath, $clips_info_file_name){
    $pathToDataClassesFile = $directoryVideoPath . "/" . $clips_info_file_name;
    $myfile = fopen($pathToDataClassesFile, "r") or die("Unable to open file!");
    
    $numberOfExamples = 0;
    
    //iterar sobre o ficheiro
    while(!feof($myfile)) {
        fgets($myfile);
        $numberOfExamples += 1;
    }
    fclose($myfile);
    
    return $numberOfExamples;    
}


function isRegistered($directoryVideoPath, $index, $type, $clips_info_file_name){
    $pathToDataClassesFile = $directoryVideoPath . "/". $clips_info_file_name;
    $myfile = fopen($pathToDataClassesFile, "r") or die("Unable to open file!");
    
    //iterar sobre o ficheiro
    while(!feof($myfile)) {
        $line = fgets($myfile);
        
        $info = explode(";", $line );
        if(isset($info[0]) && isset($info[5])){
            $eventIndex = $info[0];
            $eventType = $info[5];
            if($eventIndex == $index && $type == $eventType){
                return true;
            }
        }
    }
    fclose($myfile);
    
    return false;
    
}









