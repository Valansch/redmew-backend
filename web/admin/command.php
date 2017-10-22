<?php
/**
* Runs specific commands against the factorio server
*/


$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : "";

switch ( strtolower( $cmd ) ) {
   case "update":
      shell_exec('/home/factorio/server/control/update');
      break;
   case "start":
      shell_exec('/home/factorio/server/control/start');
      break;
   case "restart":
      shell_exec('/home/factorio/server/control/restart');
      break;
   case "stop":
      shell_exec('/home/factorio/server/control/stop');
      break;
   case "save":
      shell_exec('tmux send-keys -t live test Enter');
      break;
   default:
      // No known command
}

header('Location: ./');
?>
