<html>
<head>
<meta http-equiv="refresh" content="3;./" />
</head>

<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

?>



<?php 
if (!isset($_SERVER['PHP_AUTH_USER'])) {
header('WWW-Authenticate: Basic realm="Redmew Admin Console"');
header('HTTP/1.0 401 Unauthorized');
die('You\'re going to need to go ahead and authenticate');
}

$load = !is_null($_POST["load"]) && $_POST["load"] == "true";
var_dump($_POST);
$target_file = "uploads/" . basename($_FILES["fileToUpload"]["name"]) ;
$uploadOk = 1;
$fileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
if(isset($_POST["submit"])) {
	if ($_FILES["fileToUpload"]["size"] > 50000000){
		echo "Sorry, your file is too large.";
		$uploadOk = 0;
	}
	// Allow certain file formats
	if($fileType != "zip")  {
	    echo "Sorry, only ZIP files are allowed.";
	    $uploadOk = 0;
	}
	if ($uploadOk == 0) {
	    echo "Sorry, your file was not uploaded.";
	} else {
		$files = glob('uploads/*'); // get all file names
		foreach($files as $file){ // iterate files
			if(is_file($file)) unlink($file); // delete file
		}
		if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
			echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
			chmod($target_file, 0666);
			include("factorioserver.php");	
			if ($load){
				(New FactorioServer())->serverControl("loadsave web/admin/" . $target_file);
			} else {
				(New FactorioServer())->serverControl("fo mv ../web/admin/" . $target_file . " " . basename($target_file));		
			}
		} else {	
			echo "Sorry, there was an error uploading your file.";
		}
	}	
}
?>
</html>
