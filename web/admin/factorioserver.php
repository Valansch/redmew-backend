<?php

class FactorioServer {
   public $cwd = "";
   public $factorio_pid = -1;
   public $factorio_status = "Unknown";
   public $control_pid = -1;
   public $control_status = "Unknown";

   private $_log_dir = "/log/";
   private $_log_name = "live.log";

   public function __construct() {
      $web_cwd = realpath(dirname(__FILE__));
      $this->cwd = realpath( $web_cwd . "/../../");

      $factorio_bin = $this->cwd . "/bin/x64/factorio";

      $this->control_pid = file_get_contents($this->cwd . "/control_pid");
      exec("ps --pid " . $this->control_pid . " -o comm=", $output, $return_var);
      if ( $output[0] !== "start.py" ) {
         $this->control_pid = -1;
      }

      // Find pid
      exec("ps ahxwwo pid,command", $output);
      foreach ( $output as $k => $v ) {
         if (strpos($v, $factorio_bin) !== false) {
            // print "Found it! -- ".  $v;
            $this->factorio_pid = (int)substr($v, 1, strpos($v, " ",2) - 1);
         }
      }

      $this->factorio_status = ( $this->factorio_pid > 0 ) ? "Running" : "Not running";
      $this->control_status = ( $this->control_pid > 0 ) ? "Running" : "Not running";
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

   public function helpTMux() {
return "tmux new -s dev
ctrl + B
:split-window -v
tail -f log/live.log
ctrl + B + arrow-up
" . $this->cwd . "/start.py";

   }
}
