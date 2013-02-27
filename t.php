<?php


if(isset($_FILES['file']['name'])){
$target_path = "upload/";
$target_path = $target_path . basename( $_FILES['file']['name']); 

if(move_uploaded_file($_FILES['file']['tmp_name'], $target_path)) {
    
  } 
}
else{

	echo '{
    "batch": false, 
    "scr_img": "1"}';
}
?>