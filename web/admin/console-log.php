<?php
/**
 * Reads the status of the server, and returns a JSON array
 * @TODO -- Make it do that!
 */

 include("factorioserver.php");

$Server = new FactorioServer();

$currentLog = $Server->getLog();

print implode("<br />", explode( "\n", $currentLog) );
