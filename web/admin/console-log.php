<?php
/**
 * Reads the status of the server, and returns a JSON array
 * @TODO -- Make it do that!
 */

 include("factorioserver.php");

$Server = new FactorioServer();

if ( isset($_GET["all"] ) ) {
   $currentLog = $Server->getLogDownload();

   header("content-type: text/plain");
   echo ( file_get_contents( $currentLog ));
} else {
   $currentLog = $Server->getLog();
   print implode("<br />", explode( "\n", $currentLog) );

}
