<!DOCTYPE html>


<?php 

include_once './Lib/lib.php';

$directory_path = "videos/vid_20_08_2022_17_22/";
$nr_files = getDirNumberOfFiles($directory_path);

# $classes = getClassesName($directory_path); 
$classes = array("ball_hit", "noise");


?>

<html>
    <head>
        <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
        <title>yo</title>
        
        
        <script type="text/javascript" src="Lib/jsScripts.js">
        </script>
    </head>
    <body>
        <div><!-- contentor raiz -->
            <select id="cars" name="cars" onchange="SelectEventsOnChange(this)">
                <option value="none"></option>
                <option value="all">all</option>
                <option value="ball_hit">ball-hit</option>
                <option value="noise">noise</option>
            </select>
            
        </div>
        
        <div id = "container">
            County:<br>
            <select
              name="county" 
              id="county" 
              size="1">
            </select><br>
            
        </div>
        
        
    </body>
</html>
