<?php

 
if (!isset($_SERVER['PHP_AUTH_USER'])) {
header('WWW-Authenticate: Basic realm="Redmew Admin Console"');
header('HTTP/1.0 401 Unauthorized');
die('You\'re going to need to go ahead and authenticate');
}



$str = str_replace("</div>", "", str_replace("<div>", "", (str_replace("&nbsp;", "", str_replace("<br>", "", $_POST["description"])))));
$json = json_decode($str, true);
if (  is_null( $json) ) {
  echo("Invalid Json Syntax\n");
  echo $str;
} else {
  include("factorioserver.php");
  $Server = new FactorioServer();
  $Server->sendDescription( $json );
}

