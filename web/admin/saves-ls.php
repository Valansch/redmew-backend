<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
?>
<?php

 
if (!isset($_SERVER['PHP_AUTH_USER'])) {
header('WWW-Authenticate: Basic realm="Redmew Admin Console"');
header('HTTP/1.0 401 Unauthorized');
die('You\'re going to need to go ahead and authenticate');
}



$arr = [];
foreach(scandir("/home/factorio/server/saves/") as $item) {
	if (!is_dir("/home/factorio/server/saves/" . $item)) {
		$elem = [];
		$elem["name"] = $item;
		$elem["size"] = filesize("/home/factorio/server/saves/" . $item);
		$elem["timestamp"] = filemtime("/home/factorio/server/saves/" . $item);
		array_push($arr, $elem);
	}
};
echo(json_encode(array_values($arr)));

?>
