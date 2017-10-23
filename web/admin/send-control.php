<?php
/**
 * control the server
 */

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
      default:
   }

}
