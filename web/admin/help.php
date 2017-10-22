<?php
/**
 * Reads the status of the server, and returns a JSON array
 * @TODO -- Make it do that!
 */

 include("factorioserver.php");

$Server = new FactorioServer();

$topic = isset( $_GET["topic"] ) ? $_GET["topic"] : "";

switch ( $topic ) {
   case "tmux" :
      print $Server->helpTMux();
      break;

}
