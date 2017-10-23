<?php
/**
 * Reads the status of the server, and returns a JSON array
 * @TODO -- Make it do that!
 */

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
   $currentLog = $Server->getLog();
   print implode("<br />", explode( "\n", $currentLog) );

}
