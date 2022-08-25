<!DOCTYPE html>
<html>
    <head>
        <meta ttp-equiv='Content-Type' content='text/html; charset=utf-8'>
        <title>User Analysis</title>
        
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        
        <link REL="stylesheet" TYPE="text/css" href="Lib/jsScripts.js">
    </head>

    <body>  
    <?php
    
    include_once './Lib/lib.php';
    include './Lib/constants.php';
        
    $method = $_SERVER[ 'REQUEST_METHOD' ];
  
    if ( $method=='POST') {
      $_INPUT_METHOD = INPUT_POST;
	  $_ARGS = $_POST;
    } elseif ( $method=='GET' ) {
      $_INPUT_METHOD = INPUT_GET;
	  $_ARGS = $_GET;
    }
    else {
      echo "Invalid HTTP method (" . $method . ")";
      exit();
    }

    
    $flags[] = FILTER_NULL_ON_FAILURE;
    
    $numberOfExamples = getNumberOfExamples($directoryVideoPath);
    
    //phpinfo(); // para alterar o número de váriáveis enviadas para o servidor a cada pedido
    
    // o método POST só recebe as alterações!
    $numberOfUserReviews = getDirNumberOfFiles($userAnalysisDirPath); 
    $file = fopen($userAnalysisDirPath . "/" . "user_review_" . $numberOfUserReviews, "w") 
            or die("Unable to open file!");
    
    $writedContent = array();
    for($i = 0; $i < $numberOfExamples; $i++){
        $ini_fin = $_POST['hidden'.$i];
        if($ini_fin === "" || $ini_fin === NULL){
            continue;
        }
        
        $lineInfo = explode("_", $ini_fin);
        $type = $lineInfo[0];
        $index = $lineInfo[1];
        $ini_idx = $lineInfo[2];
        $fin_idx = $lineInfo[3];
        
        if(!isRegistered($directoryVideoPath, $index, $type)){
            fwrite($file, $ini_fin ."\n");
            $writedContent[] = $ini_fin;
        }
    } 
    
    fclose($file);
    
    $numberLinesWrited = count($writedContent);
    if($numberLinesWrited == 0){
        echo "You did not make any changes.";
    }
    
    else{
        echo "<p>Registered changes</p>";
        echo "<div class='userChangesDiv'>";
        for($i = 0; $i < $numberLinesWrited; $i++){
            echo "<p class='registedLine'>" . $writedContent[$i] . "</p>";
        }
        
        echo "</div>";
    }
    
    echo "<br>";
    echo "<br>";
    echo "<hr>";
    echo "<button class='backButton' onclick='history.back()'>Back</button>";
    
    ?>
        
    
    </body>
</html>
