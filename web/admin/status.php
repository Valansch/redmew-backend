<?php
/**
 * Reads the status of the server, and returns a JSON array
 * @TODO -- Make it do that!
 */

 include("factorioserver.php");

$Server = new FactorioServer();

$output = [
   "cwd" => $Server->cwd,
   "pid" => $Server->pid,
   "status" => $Server->status
];
print json_encode($output);
