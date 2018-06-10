<?php
/**
 * control the server
 */
 
error_reporting(E_ALL);
ini_set('display_errors', 1);

?>

<?php
if (!isset($_SERVER['PHP_AUTH_USER'])) {
header('WWW-Authenticate: Basic realm="Redmew Admin Console"');
header('HTTP/1.0 401 Unauthorized');
die('You\'re going to need to go ahead and authenticate');
}


$control = isset( $_GET["control"] ) ? $_GET["control"] : "";

if (  ! empty( $control ) ) {

   include("factorioserver.php");

   $Server = new FactorioServer();
   switch ( $control ) {
      case "update":
      case "start":
      case "restart":
      case "stop":
      case "save":
         $Server->serverControl( $control );
         break;
      case "restart_script": 
      	 exec('echo restart > /home/factorio/server/restart');
      default:
   }

}
?>
