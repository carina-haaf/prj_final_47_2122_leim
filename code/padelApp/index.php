<!DOCTYPE html>

<?php 

include_once './Lib/lib.php';
include './Lib/constants.php';

$classes = getDataClasses($directoryVideoPath);
$firstClipName = getFirstClipName($directoryVideoPath);
$firstIniAndFin = getFirstClipIniAndFin($directoryVideoPath);
$numberOfExamples = getNumberOfExamples($directoryVideoPath);
?>

<html>
    <head>
        <meta http-equiv='Content-Type' 
              content='text/html; charset=utf-8'>
        <title>yo</title>
        
        <link REL="stylesheet" TYPE="text/css" href="Lib/styles.css">
        
        <script type="text/javascript" src="Lib/jsScripts.js">
        </script>
        
        <link rel="shortcut icon" href="#">
    </head>
    
    <body onload='SelectAllEvents("<?php echo $directoryVideoPath; ?>"); 
        LoadClasses(<?php echo json_encode($classes); ?>); 
        LoadVideo(<?php echo json_encode($directoryVideoPath); ?>, <?php echo json_encode($firstClipName); ?>); '>
        
        <!-- hidden element -->
        <input id="nrOfEvents" type="hidden" value="<?php echo $numberOfExamples; ?>" >
        
        <!-- contentor raiz -->
        <div>
            
            <!-- contentor onde está o filtro -->
            <div id = "topDiv" class="topDiv"> 
                <select id="classSelect" onchange="SelectEventsOnChange(this, '<?php echo $directoryVideoPath; ?>');">
                    <option value="all">all</option>
                </select><br><br>
            </div>
            
            
                       
            <!-- contentor onde estão os selects e o video -->
            <div id = "middleDiv" class="middleDiv">
                
                
                
                <div id = "selectsContainer" class="selectsContainer">
                </div> 
                
                <div class="videoContainer">
                    
                    <div id = "videoDiv" class="videoDiv">
                        <p><?php echo "Selected period: " . $firstIniAndFin[0] . " - " . $firstIniAndFin[1] ; ?></p>

                    </div>

                    <div id = "previousNextDiv" class="previousNextDiv">
                        <button id='next' onclick='GetPreviousClip("<?php echo $directoryVideoPath; ?>", document.getElementById("video").getAttribute("name"))'>Previous</button>
                        <button id='previous' onclick='GetNextClip("<?php echo $directoryVideoPath; ?>", document.getElementById("video").getAttribute("name"))'>Next</button>
                    </div>
                    
                </div>
                
                
                
            </div>           
            
           
        
        
        </div> 
        
    </body>
</html>
