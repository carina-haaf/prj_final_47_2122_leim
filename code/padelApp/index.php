<!DOCTYPE html>

<?php 

include_once './Lib/lib.php';
include_once './Lib/constants.php';

$array = getVideoDirNames($videosDirPath);
$hostname = "http://localhost:4000/";


?>

<html>
    <head>
        <meta http-equiv='Content-Type'
              content='text/html; charset=utf-8'>
        <title>Homepage</title>
        
        <link REL="stylesheet" TYPE="text/css" href="Lib/styles.css">
        
        <script type="text/javascript" src="Lib/jsScripts.js">
        </script>
        
        <script>
            
        
        </script>
        
        <link rel="shortcut icon" href="#">
       
    </head>
    
    <body>
        <p class="title">Available Videos</p>
        
        <?php
        
        if($array == NULL){
            echo "<p class='noVideosWarning'>No videos available!</p>";
        }
        
        else{
            for($i = 0; $i < count($array); $i++){ ?>
        
            <a href="<?php echo $link . "videoAnnotation.php?video=" . $array[$i] ?>"
               class="availableVideos">
                <?php echo $array[$i] ?></a><br><br>
        
        <?php }} ?>
        
        
    </body>
</html>
