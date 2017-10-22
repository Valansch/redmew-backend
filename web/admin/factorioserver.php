<?php

class FactorioServer {
   public $cwd = "";
   public $pid = -1;
   public $status = "Unknown";

   private $_log_dir = "/";
   private $_log_name = "factorio-current.log";

   public function __construct() {
      $web_cwd = realpath(dirname(__FILE__));
      $this->cwd = realpath( $web_cwd . "/../../");

      $factorio_bin = $this->cwd . "/bin/x64/factorio";

      // Find pid
      exec("ps ahxwwo pid,command", $output);
      foreach ( $output as $k => $v ) {
         if (strpos($v, $factorio_bin) !== false) {
            // print "Found it! -- ".  $v;
            $this->pid = (int)substr($v, 1, strpos($v, " ",2) - 1);
         }
      }

      if ( $this->pid > 0 ) {
         $this->status = "Running";
      } else {
         $this->status = "Not running";
      }
   }

   public function startServer() {
      $cwd = $this->cwd;
      $cmd = $cwd . "/bin/x64/factorio"
           . " --server-setting " . $cwd . "/server-settings.json"
           . " --start-server " . $cwd . "/saves/_autosave1.zip"
           . " --console-log " . $cwd . $this->_log_dir . $this->_log_name
           // . $cwd . " --bind 5.9.164.209"
      ;
      exec( $cmd, $output, $return_var);

      var_dump($output);
      var_dump($return_var);
   }


   public function getLog($lines = 50) {
      $output_tmp = "/tmp/current_log_output.log";
      $command = "tail " . $this->cwd . $this->_log_dir . $this->_log_name . " --lines " . $lines . " > " . $output_tmp;
      // print $command;
      exec($command);

      return file_get_contents( $output_tmp );
   }

   public function sendCommand( $server_command ) {
      $command = "echo " . escapeshellarg( $server_command . "\n" ) . " > /proc/" . $this->pid . "/fd/0";
      print $command;
      exec( $command , $output, $return_var );

      var_dump($return);

   }

}
