<?php
/**
 * Sends commands to the server
 */

$command = isset( $_POST["command-to-send"] ) ? $_POST["command-to-send"] : "";

if (  ! empty( $command) ) {

    include("factorioserver.php");

   $Server = new FactorioServer();

   $Server->sendCommand( $command );

}
