<html>
<head>
   <title>redmew: Factorio Server Control</title>
   <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
   <link rel="stylesheet" type="text/css" href="factorio.css">
   <link rel="stylesheet" type="text/css" href="redmew.css">

   <script type="text/javascript">
   // var window.server_status;

   $(document).ready(function () {
      $.getJSON("status.php", function (json) {
         window.server_status = json;
         init_controls();
      });

      $("#console .output").load("console-log.php", function () { $(this).scrollTop($(this)[0].scrollHeight); } );
   });

   function init_controls() {
      $("#controlPID").html( window.server_status.control_pid );
      $("#factorioPID").html( window.server_status.factorio_pid );
      $("#factorioStatus").html( window.server_status.factorio_status );

      if ( window.server_status.control_status != "Running") {
         $("#help-StartTMux").show();
         $("#help-StartTMux xmp").load("help.php?topic=tmux");
         $("#serverControl ul").hide();
      } else {
         $("#serverControl ul").show();

         if ( window.server_status.factorio_status == "Running" ) {
            $("#factorioStart").hide();
            $("#factorioStop").show();
            $("#factorioRestart").show();
            $("#factorioUpdate").show();
            $("#factorioSave").show();
         } else {
            $("#factorioStart").show();
            $("#factorioStop").hide();
            $("#factorioRestart").hide();
            $("#factorioUpdate").hide();
            $("#factorioSave").hide();
         }
      }


   }


   </script>
</head>
<body>
   <h1>redmew: Factorio Server Control</h1>

   <div id="serverControl">
      <h2>Server Command and Control</h2>
      <dl>
         <dt>Control PID</dt>
         <dd id="controlPID"></dd>
         <dt>Server PID</dt>
         <dd id="factorioPID"><dd>
         <dt>Server Status</dt>
         <dd id="factorioStatus"></dd>
      </dl>
      <ul>
         <li id="factorioStart"><a href="send-control.php?control=start" class="btn btn-custom btn-large btn-block">Start</a></li>
         <li id="factorioStop"><a href="command.php?cmd=stop" class="btn btn-custom btn-large btn-block">Stop</a></li>
         <li id="factorioRestart"><a href="command.php?cmd=restart" class="btn btn-custom btn-large btn-block">Restart</a></li>
         <li id="factorioUpdate"><a href="command.php?cmd=update" class="btn btn-custom btn-large btn-block">Update</a></li>
         <li id="factorioSave"><a href="command.php?cmd=save" class="btn btn-custom btn-large btn-block">Save</a></li>
      </ul>

      <div id="help-StartTMux">
         <strong>Server control session not found. Please start the tmux using:</strong>
         <xmp></xmp>
      </div>
   </div>

   <div id="serverStatus">
      <h2>Server Status</h2>
      <p>Todo - Convert to async JS call, send output to a div</p>
      <div class="output"></div>
   </div>

   <div id="chat">
      <h2>Chat</h2>
      <p>Todo - Convert to async JS call, send output to a div</p>
      <div class="output"></div>
   </div>

   <div id="console">
      <h2>Server Console</h2>
      <div class="output"></div>
      <form method="post" action="send-command.php">
         <input type="text" name="command-to-send" />
         <input type="submit" />
      </form>
   </div>

</body>
</html>
