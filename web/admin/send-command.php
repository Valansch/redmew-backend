<?php
/**
 * Sends commands to the server
 */

 
if (!isset($_SERVER['PHP_AUTH_USER'])) {
header('WWW-Authenticate: Basic realm="Redmew Admin Console"');
header('HTTP/1.0 401 Unauthorized');
die('You\'re going to need to go ahead and authenticate');
}



$command = isset( $_POST["command"] ) ? $_POST["command"] : "";

if ( !  empty( $command) ) {
    include("factorioserver.php");

   $Server = new FactorioServer();

   print $Server->sendCommand( $command );

}
?>
