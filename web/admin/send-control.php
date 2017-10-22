<?php
/**
 * control the server
 */

$control = isset( $_GET["control"] ) ? $_GET["control"] : "";

if (  ! empty( control) ) {

   include("factorioserver.php");

   $Server = new FactorioServer();
   switch ( $control ) {
      case "update":
         break;
      case "start":
         $Server->startServer();
         break;
      case "restart":
         break;
      case "stop":
         break;
      case "save":
         break;
      default:
   }

}
