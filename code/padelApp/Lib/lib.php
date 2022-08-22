<?php


function getDirNumberOfFiles($directory){
    
    $files = scandir($directory);    

    return count($files) - 2;
}


function get($directoryVideoPath, $desiredType="all"){
    // abrir o ficheiro
    $pathToDataClassesFile = $directoryVideoPath . "/clips_info.txt";
    $myfile = fopen($pathToDataClassesFile, "r") or die("Unable to open file!");
    
    //iterar sobre o ficheiro
    while(!feof($myfile)) {
        $line = fgets($myfile);

        // colocar no array: indice, t_ini, t_fin, nome do mini clip
        // mas antes garantir que estes valores existem
        $info = explode(";", $line );
        if(isset($info[0]) && isset($info[3]) && isset($info[4]) && 
                isset($info[5]) && isset($info[6])){
            $index = $info[0];
            $type = $info[5];
            $ini = $info[3];
            $fin = $info[4];
            $name = $info[6];
        }
        
        // caso se queira só os clips de uma classe não vale a pena
        // colocar os exemplos de outras classes também
        if( ($type !== $desiredType && $desiredType !== "all")){continue;}
                
        $result[] = array(
            'index'=>$index, 
            'type'=> $type,
            'ini' => $ini,
            'fin' => $fin,
            'name' => $name);
    }
    fclose($myfile);
    sort($result);
    
    return $result;
    
}


function getVideoClass($videoName){
    
}

function getVideoNumber($videoName){
    
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
    








