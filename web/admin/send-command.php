<?php
/**
 * Sends commands to the server
 */

$command = isset( $_POST["command"] ) ? $_POST["command"] : "";

if (  ! empty( $command) ) {
    include("factorioserver.php");

   $Server = new FactorioServer();

   print $Server->sendCommand( $command );

}
?>
