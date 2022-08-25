<!DOCTYPE html>

<?php 

include_once './Lib/lib.php';
include './Lib/constants.php';

$classes = getDataClasses($directoryVideoPath);
$firstClipName = getFirstClipName($directoryVideoPath);
$firstIniAndFin = getFirstClipIniAndFin($directoryVideoPath);
$numberOfExamples = getNumberOfExamples($directoryVideoPath);
$currentVideoName = $videoName;

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
            
            <form enctype="multipart/form-data"
                    action="processForm.php"
                    method="POST" >
                
                <div>
                    <p class="title">Video in Analysis: <?php echo $currentVideoName; ?></p>
                    
                </div>
                
                <!-- contentor onde estão os selects e o video -->
                <div id = "middleDiv" class="middleDiv">
                    
                    
                    
                    <div class="videoContainer">

                        <div id = "videoDiv" class="videoDiv">
                            <!-- <p><?php echo "Selected period: " . $firstIniAndFin[0] . " - " . $firstIniAndFin[1] ; ?></p> -->

                        </div>

                        <div id = "previousNextDiv" class="previousNextDiv">
                            <input class="previousButton" type="button" value="Previous <" id='previous' onclick='GetPreviousClip("<?php echo $directoryVideoPath; ?>", document.getElementById("video").getAttribute("name"))'> 
                            <input class="nextButton" type="button" value="> Next" id='next' onclick='GetNextClip("<?php echo $directoryVideoPath; ?>", document.getElementById("video").getAttribute("name"))'>
                        </div>

                    </div>
                    
                    <div id = "eventsContainer" class="eventsContainer">
                        
                        <!-- contentor onde está o filtro -->
                        <div id = "filterDiv" class="filterDiv"> 
                            <select id="classSelect" onchange="SelectEventsOnChange(this, '<?php echo $directoryVideoPath; ?>');">
                                <option value="all">all</option>
                            </select>
                            
                            <text class="start_time">Start Time</text>
                            <text class="end_time">End Time</text>
                        </div>
                        
                        
                        <div id = "selectsContainer" class="selectsContainer">
                        </div>
                        
                        <div id = "bottomDiv" class="bottomDiv">
                    
                            <div class="buttonDiv">
                                <input class="formButton" type="submit" name="Submit" value="Submit">
                                <input class="formButton" type="reset" name="Reset" value="Reset">
                            </div>

                        </div> 
                        
                        
                    </div>
                                       
                </div>
            
                <br>

            </form>
            
        </div>
        
    </body>
</html>
