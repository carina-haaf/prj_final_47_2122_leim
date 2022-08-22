<!DOCTYPE html>


<?php 

include_once './Lib/lib.php';
include './Lib/constants.php';

$classes = getDataClasses($directoryVideoPath);
    
?>

<html>
    <head>
        <meta http-equiv='Content-Type' 
              content='text/html; charset=utf-8'>
        <title>yo</title>
        
        <link REL="stylesheet" TYPE="text/css" href="Lib/styles.css">
        
        
        <script type="text/javascript" src="Lib/jsScripts.js">
        </script>
    </head>
    <body onload='SelectAllEvents(); 
        LoadClasses(<?php echo json_encode($classes); ?>)'>
        
        <!-- contentor raiz -->
        <div>
            
            <!-- contentor onde está o filtro -->
            <div id = "topDiv" class="topDiv"> 
                <select id="classSelect" onchange="SelectEventsOnChange(this)">
                    <option value="all">all</option>
                </select><br><br>
            </div>
            
            
            <script type="text/javascript">
            </script>
            
            <!-- contentor onde estão os selects e o video -->
            <div id = "middleDiv" class="middleDiv">
                
                
                
                <div id = "selectsContainer" class="selectsContainer">
                </div> 
                
                
                
                <div id = "videoDiv" class="videoDiv">
                    <video id="vid" width="400" controls >
                        <source src="videos/vid_20_08_2022_17_22/hits/clip_101_ball_hit.mp4" 
                                type="video/mp4" >
                        Your browser does not support the video tag.
                    </video>
                    <!-- videos/vid_20_08_2022_17_22/hits/clip_101_ball_hit.mp4#t=2,5 -->
                  
                
                </div>
                
                
            </div>           
        
        
        
        </div> 
        
    </body>
</html>
