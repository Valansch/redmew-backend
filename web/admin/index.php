<html>
<head>
   <title>redmew: Factorio Server Control</title>
   <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
   <link rel="stylesheet" type="text/css" href="factorio.css">
   <link rel="stylesheet" type="text/css" href="redmew.css">

   <script type="text/javascript">
   // var window.server_status;
   var  serverControlTimeout = null;
   var serverConsoleTimeout = null
   var timePollControl = 5000;
   var timePollConsole = 3000;

   $(document).ready(function () {
      reloadStatus();
      reloadConsole();
      $("#command").focus();

      $("#serverControl ul a").click(function (e) {
         e.preventDefault();

         href = $(this).attr("href");
         $("#serverControl .output").load(href);
         $("#serverControl ul a").addClass("wait");

         window.clearTimeout(serverControlTimeout);
         serverControlTimeout = window.setTimeout(reloadStatus, timePollControl);

      });

      $("form").submit(function (e) {
         e.preventDefault();
         command = $("#command").val();
         $.ajax({
           type: "POST",
           url: $(this).attr("action"),
           data: { command: command }
         });
         reloadConsole();
         $("#command").val("");
      });
   });

   function serverControlButtonEnable() {
      $("#serverControl ul a").removeClass("wait");
   }

   function reloadStatus() {
      window.clearTimeout(serverControlTimeout);

      $.getJSON("status.php", function (json) {
         window.server_status = json;
         init_controls();
         serverControlButtonEnable();

         serverControlTimeout = window.setTimeout(reloadStatus, timePollControl);
      });
   }

   function reloadConsole() {
      window.clearTimeout(serverConsoleTimeout);

      $("#console .output").load("console-log.php", function () {
         $(this).scrollTop($(this)[0].scrollHeight);
         serverConsoleTimeout = window.setTimeout(reloadConsole, timePollConsole);
      });

   }

   function init_controls() {
      $("#controlPID").html( window.server_status.control_pid + " / " + window.server_status.control_port);
      $("#factorioPID").html( window.server_status.factorio_pid + " / " + window.server_status.factorio_status );
      $("#factorioName").html( window.server_status.serverSettings.name );
      $("#factorioDescription").html( window.server_status.serverSettings.description );
      $("#factorioTags").html( window.server_status.serverSettings.tags.join("<br />") );

      if ( window.server_status.control_status != "Running") {
         $("#help-StartTMux").show();
         $("#help-StartTMux xmp").load("help.php?topic=tmux");
         $("#serverControl ul").hide();
      } else {
         $("#help-StartTMux").hide();
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
      <p>@TODO: Player Count / List</p>
      <dl>
         <dt>Control Script</dt>
         <dd id="controlPID"></dd>
         <dt>Factorio</dt>
         <dd id="factorioPID"><dd>
         <dt>Server Name</dt>
         <dd id="factorioName"></dd>
         <dt>Description</dt>
         <dd id="factorioDescription"></dd>
         <dt>Tags</dt>
         <dd id="factorioTags"></dd>
      </dl>
      <ul>
         <li id="factorioStart"><a href="send-control.php?control=start" class="btn btn-custom btn-large btn-block">Start</a></li>
         <li id="factorioStop"><a href="send-control.php?control=stop" class="btn btn-custom btn-large btn-block">Stop</a></li>
         <li id="factorioRestart"><a href="send-control.php?control=restart" class="btn btn-custom btn-large btn-block">Restart</a></li>
         <li id="factorioUpdate"><a href="send-control.php?control=update" class="btn btn-custom btn-large btn-block">Update</a></li>
         <li id="factorioSave"><a href="send-control.php?control=save" class="btn btn-custom btn-large btn-block">Save</a></li>
      </ul>

      <div class="output"></div>

      <div id="help-StartTMux">
         <strong>Server control session not found. Please start the tmux using:</strong>
         <xmp></xmp>
      </div>
   </div>

   <div id="console">
      <h2>Server Console</h2>
      [ <a href="console-log.php?all=all" target="_blank">Full Log</a> ]
      <div class="output"></div>
      <form method="post" action="send-command.php">
         <input type="text" autocomplete="off" id="command" name="command" />
         <input type="submit" value="Send" />
      </form>
   </div>

</body>
</html>
