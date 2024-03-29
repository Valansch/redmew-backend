<?php
/**
 * Reads the status of the server, and returns a JSON array
 * @TODO -- Make it do that!
 */
 
if (!isset($_SERVER['PHP_AUTH_USER'])) {
header('WWW-Authenticate: Basic realm="Redmew Admin Console"');
header('HTTP/1.0 401 Unauthorized');
die('You\'re going to need to go ahead and authenticate');
}


 include("factorioserver.php");

$Server = new FactorioServer();

if ( isset($_GET["all"] ) ) {
   $path = $Server->getLogDownload();

   $public_name = basename($path);

   // get the file's mime type to send the correct content type header
   $finfo = finfo_open(FILEINFO_MIME_TYPE);
   $mime_type = finfo_file($finfo, $path);

   // send the headers
   header("Content-Disposition: inline; filename=$public_name;");
   header("Content-Type: $mime_type");
   header('Content-Length: ' . filesize($path));

   // stream the file
   $fp = fopen($path, 'rb');
   fpassthru($fp);

} else {
   $lines = 20;;
   if (isset($_GET["lines"])) $lines = (int)$_GET[lines];
   
   $currentLog = $Server->getLog($lines);
   print implode("<br />", explode( "\n", $currentLog) );

}
