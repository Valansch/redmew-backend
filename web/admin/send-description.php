<?php

$str = str_replace("&nbsp;", "", str_replace("<br>", "", $_POST["description"]));
$json = json_decode($str, true);
if (  is_null( $json) ) {
  echo("Invalid Json Syntax");
} else {
  include("factorioserver.php");
  $Server = new FactorioServer();
  $Server->sendDescription( $json );
}

