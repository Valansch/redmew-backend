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

      $this->control_pid = file_exists($this->cwd . "/control_pid") ? file_get_contents($this->cwd . "/control_pid") : -1;
      if ( ! is_numeric( $this->control_pid ) || ! posix_getpgid ($this->control_pid) ) {
         $this->control_pid = -1;
      }

      $this->factorio_pid = file_exists($this->cwd . "/factorio_pid") ? file_get_contents($this->cwd . "/factorio_pid") : -1;
      if ( ! is_numeric( $this->factorio_pid ) || ! posix_getpgid ($this->factorio_pid) ) {
         $this->factorio_pid = -1;
      }

      $this->factorio_status = ( $this->factorio_pid > 0 ) ? "Running" : "Not running";
      $this->control_status = ( $this->control_pid > 0 ) ? "Running" : "Not running";
   }

   public function serverControl($control) {
      $this->_sendControl($control);
   }

   private function _sendControl( $contents ) {
      $dir =  "/tmp/command_pipeline" . $this->cwd;

      $parts = explode('/', $dir);
      $file = "pipe";
      $dir = '';
      foreach($parts as $part) {
         if ( !empty($part) ) {
            if (!is_dir($dir .= "/$part") ) {
               mkdir($dir);
            }
         }
      }

      file_put_contents("$dir/$file", $contents . "\n");
      chmod("$dir/$file", 0777);
   }


   public function getLog($lines = 20) {
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
