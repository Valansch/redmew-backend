<?php
if (!isset($_SERVER['PHP_AUTH_USER'])) {
   header('WWW-Authenticate: Basic realm="Redmew Admin Console"');
   header('HTTP/1.0 401 Unauthorized');
   die('You\'re going to need to go ahead and authenticate');
}

$user = $_SERVER['PHP_AUTH_USER'];
$pass = $_SERVER['PHP_AUTH_PW'];

include("auth_data.php");

if ( ! isset($auth_admins[$user]) ) {
   header('WWW-Authenticate: Basic realm="My Realm"');
   header('HTTP/1.0 401 Unauthorized');
   die ("Nope, no bueno");
}

$pw_hash = $auth_admins[$user];

$validated = password_verify( $pass, $pw_hash );

if (!$validated) {
  header('WWW-Authenticate: Basic realm="My Realm"');
  header('HTTP/1.0 401 Unauthorized');
  die ("Nope, no bueno");
}
?>
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
   var description_open = false;
   $(document).ready(function () {
      reloadStatus();
      reloadConsole();
      lsSaves("name");
      setSelectionButtonsEnabled(false);
      $("#command").focus();
      $("#description").hide();
      $("#saveDescriptionBox").hide();
      $("#toggle_description").click(function (e) {
         e.preventDefault();
	 if (description_open) {
	    $("#toggle_description").text("Edit Description");
	    $("#saveDescriptionBox").hide();
	    $("#description").hide();
	} else {
	    $("#toggle_description").text("Cancel");
	    $("#saveDescriptionBox").show();
	    $("#description").show();
	    loadDescription();
	}
	description_open = ! description_open;
      });
      $("#saveDescription").click(function (e) {
         var description = $("#description").html();
	 $.ajax({
           type: "POST",
           url: "send-description.php",
           data: {description : description},
	   success: function(html) { 
	      if (html != "") {
	         alert(html);
              } else {
                 $("#toggle_description").click();   
                 reloadStatus();
	      }
	   },
           error: function(error) {console.log(error);}
	});
      });
      $("#serverControl ul a").click(function (e) {
         e.preventDefault();
         if ($(this).attr("id") == "upload_link") {
	    e.preventDefault();
            $("#upload_select").trigger('click');
            return;
	 }
         href = $(this).attr("href");
         $("#dummy_output").load(href);
         $("#serverControl ul a").addClass("wait");
         $("#saveSelectionWrapper #loadSel").addClass("wait");

	window.clearTimeout(serverControlTimeout);
         serverControlTimeout = window.setTimeout(reloadStatus, timePollControl);

      });
      $("#command_form").submit(function (e) { 
	 e.preventDefault();
         command = $("#command").val();
         if (command.charAt(0) != '/' && command.charAt(0) != ':') {
            name = '<?php print $_SERVER['PHP_AUTH_USER']; ?>';
            var msg = "'[" + name + "@Server]: " + command + "'";
            command = "/silent-command game.print(" + msg +  ")  log(" + msg + ")";
         } 
         $.ajax({
           type: "POST",
           url: $(this).attr("action"),
           data: { name : name, command: command }
         });
         reloadConsole();
         $("#command").val("");
      });
      $("#upload_select").change(function (){
        $("#btnUpload").click();	
      });

      $("#deleteSel").click(function (e){
     	if (confirm("Do you really want to delete " + saves[selectedSave]["name"] + "?")){
	  send_command(":fo rm " + saves[selectedSave]["name"]);	
	}
      });

      $("#moveSel").click(function (e){
     	if (confirm("Do you really want to archive " + saves[selectedSave]["name"] + "?")){
	  send_command(":fo mv " + saves[selectedSave]["name"] + " archive/" + saves[selectedSave]["name"]);	
	}
      });

      $("#loadSel").click(function (e){
     	if (confirm("Do you really want to load " + saves[selectedSave]["name"] + "?")){
           send_command(":loadsave saves/" + saves[selectedSave]["name"])	
	}
      });

      $("#upload").click(function(e) {
        $("#upload_load").val("false");
      	$("#upload_select").trigger('click');
      });
      $("#renameSel").click(function (e){
     	var newname = prompt("Choose a new name for " + saves[selectedSave]["name"])
	if (newname && newname.trim() != "")
	  send_command(":fo mv " + saves[selectedSave]["name"] + " " +  newname);	
      });
   });

   function send_command(command) {
       $.ajax({
           type: "POST",
           url: "send-command.php",
           data: { command : command},
	   success: function(e) {
	   	if (e.trim() != "") {
	   		alert(e);
		}
	        window.setTimeout(reloadSaveSelection, 100);	
	   }
         });
   }

   function serverControlButtonEnable() {
      $("#serverControl ul a").removeClass("wait");
      $("#saveSelectionWrapper #loadSel").removeClass("wait");
   }
   function loadDescription() {
      $.getJSON("status.php", function (json) {
         $("#description").html(
            '{<br/>&nbsp;&nbsp;"name": "' + json.serverSettings.name + '",<br/>' + 
	    '&nbsp;&nbsp;"description": "' + json.serverSettings.description + '", <br/>' +
            '&nbsp;&nbsp;"tags": [<br/>&nbsp;&nbsp;&nbsp;&nbsp;"' + 
	       json.serverSettings.tags.join('",<br/>&nbsp;&nbsp;&nbsp;&nbsp;"') + 
	     '"<br/>&nbsp;&nbsp;]<br/>}' 
         );});
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
      var lines = parseInt($("#numLines").html());
      var url = "console-log.php";
      if (!isNaN(lines)) {
        url = "console-log.php?lines=" + lines
      }
      $("#console .output").load(url, function () {
         $(this).scrollTop($(this)[0].scrollHeight);
         serverConsoleTimeout = window.setTimeout(reloadConsole, timePollConsole);
      });

   }

   function reloadSaveSelection(){
   	saves = {};
   	selectedSave = null;
	$("#saveSelectionBody").empty();
	lsSaves(lastSortKey, true);
   }

   function tdn(n) {
      if (n < 10)
         return "0" + n;
      return n;
   }

   function formatTime(dateTime){
      return dateTime.getFullYear() + "-" +
      tdn(dateTime.getMonth() + 1) + "-" +
      tdn(dateTime.getDate()) + " " +
      tdn(dateTime.getHours()) + ":" +
      tdn(dateTime.getMinutes()) + ":" +
      tdn(dateTime.getSeconds());
   }

   function setSelectionButtonsEnabled(status) {
      $("#deleteSel").attr("disabled", !status);
      $("#loadSel").attr("disabled", !status);
      $("#renameSel").attr("disabled", !status);
      $("#moveSel").attr("disabled", !status); 
 
   }
   function rowClick(id){
   	setSelectionButtonsEnabled(true);
   	$("#row" + selectedSave).removeClass('active');
   	selectedSave = id;
   	$("#row" + selectedSave).addClass('active');
	console.log(saves[id]["name"]);
   }

   function sortByKey(a, key, reverse) {
      return a.sort(function(a, b) {
         var x = a[key]; var y = b[key];
         if (reverse)
            return ((x > y) ? -1 : ((x < y) ? 1 : 0));
         else
            return ((x < y) ? -1 : ((x > y) ? 1 : 0));
         });
   }

   function formatSize(size) {
	return Math.floor(size / 104857.6 + 0.5) / 10 + " MB";
   }

   saves = {};
   selectedSave = null;
   sortKeyReversed = {};
   sortKeyReversed["name"] = true;
   sortKeyReversed["timestamp"] = true;
   sortKeyReversed["size"] = true;
   lastSortKey = "";
   function lsSaves(sortKey, dontReverse) {
      lastSortKey = sortKey;
      if (!dontReverse)
      	sortKeyReversed[sortKey] = !sortKeyReversed[sortKey];
      $.get("saves-ls.php", function (data) { 
	var savesJson = JSON.parse(data);
	saves = sortByKey(savesJson, sortKey, sortKeyReversed[sortKey]);
	$("#saveSelectionBody").empty();
	for(let i = 0; i < saves.length; i++) {
	   let size = formatSize(saves[i]["size"]);
	   let time = formatTime(new Date(saves[i]["timestamp"] * 1000)); 
	   $("#saveSelectionBody").append('<tr class="tblRow pull" id="row' + i + '" onclick="rowClick(' + i + ')"><td>' + saves[i]["name"] + '</td><td class="pull-right">' + size + '</td><td>' + time + '</td></tr>');
	}
      });
   }


   function init_controls() { 
      $("#controlPID").html( window.server_status.control_pid + " / " + window.server_status.control_port);
      $("#factorioPID").html( window.server_status.factorio_pid + " / " + window.server_status.factorio_status );
      $("#factorioName").html( window.server_status.serverSettings.name );
      $("#factorioDescription").html( window.server_status.serverSettings.description );
      $("#factorioTags").html( window.server_status.serverSettings.tags.join("<br />") );
      if ( window.server_status.control_status != "Running") {
         $("#factorioStart").hide();
         $("#factorioLoad").hide();
         $("#factorioStop").hide();
         $("#factorioRestart").hide();
         $("#factorioUpdate").hide();
         $("#factorioSave").hide();
	 $("#descriptionBox").hide();
         $("#help-StartTMux").show();
	 $("#help-StartTMux xmp").load("help.php?topic=tmux"); 
	 $("#scriptRestart").show(); 
      } else {
         $("#help-StartTMux").hide();
         $("#serverControl ul").show();
	 $("#scriptRestart").hide();
         if ( window.server_status.factorio_status == "Running" ) {
	    $("#factorioStart").hide();
            $("#factorioLoad").show();
            $("#factorioStop").show();
            $("#factorioRestart").show();
            $("#factorioUpdate").show();
            $("#factorioSave").show();
	    $("#descriptionBox").show();
         } else {
            $("#factorioStart").show();
	    $("#factorioLoad").show();
	    $("#factorioStop").hide();
	    $("#factorioUpdate").show();
            $("#factorioRestart").hide();
            $("#factorioSave").hide();
	    $("#descriptionBox").hide();
         }
      }
   }
   </script>
</head>
<body>
   <h1>redmew: Factorio Server Control</h1>
   <div id="serverControlSaveSelectionWrapper">
      <div id="serverControl">
      	<h2>Server Command and Control</h2>
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
		<li id="scriptRestart"><a href="send-control.php?control=restart_script" class="btn btn-custom btn-large btn-block">Start Script</a></li>
        	<li id="factorioStart"><a href="send-control.php?control=start" class="btn btn-custom btn-large btn-block">Start</a></li>
        	<li id="factorioStop"><a href="send-control.php?control=stop" class="btn btn-custom btn-large btn-block">Stop</a></li>
       		<li id="factorioRestart"><a href="send-control.php?control=restart" class="btn btn-custom btn-large btn-block">Restart</a></li>
        	<li id="factorioUpdate"><a href="send-control.php?control=update" class="btn btn-custom btn-large btn-block">Update</a></li>
        	<li id="factorioSave"><a href="send-control.php?control=save" class="btn btn-custom btn-large btn-block">Save</a></li>
        	<li id="factorioLoad"><a href="" id="upload_link" class="btn btn-custom btn-large btn-block">Load</a></li>
      	</ul>
      	<form id="upload_form" action="upload.php" method="post" enctype="multipart/form-data">
         	<input id="upload_select" type="file" name="fileToUpload" />
		<input id="upload_load" name="load" value="true"/>
        	<input type="submit" value="Upload Image" name="submit" id="btnUpload" />
     	</form>
	
	<div id="help-StartTMux">
        	<strong>Server control session not found. Please start the tmux using:</strong>
        	<xmp></xmp>
      	</div>
      </div>
  


   <div id="saveSelectionWrapper"> 
      <a class="btn btn-custom btn-small" id="upload">Upload</a> 
      <a class="btn btn-custom btn-small" id="loadSel">Load</a> 
      <a class="btn btn-custom btn-small" id="renameSel">Rename</a> 
      <a class="btn btn-custom btn-small" id="moveSel">Move to archive</a> 
      <a class="btn btn-custom btn-small" id="deleteSel" >Delete</a> 
      <div id="saveSelection" class="text_box">
         <table>
	 	<thead><tr>
         		<th onclick="lsSaves('name')">Save File</th>
      	 		<th onclick="lsSaves('size')">Size</th>
	 		<th onclick="lsSaves('timestamp')">Last Modified</th>
	 	</tr><thead>
		<tbody id="saveSelectionBody">
		</tbody>
	 </table>
      </div>
   </div>
   </div>
    <div id="console">


	<div id = "description_box">
		<h3>
			[<a id="toggle_description" href="#">Edit Description</a>]
			 <div style="display: inline" id="saveDescriptionBox">[<a id="saveDescription" href="#">Save</a>]</div>
      		</h3>
		<div contentEditable class="text_box" id="description"></div>
	</div>
   	<div id="dummy_output"></div>
	<h2>Server Console</h2>
	[ <a href="console-log.php?all=all" target="_blank">Full Log</a> ]  
	[ Lines: <div contentEditable class="text_box lines" id="numLines">20</div> ]
	<p></p>


     <div class="output text_box"></div>
      <form id="command_form" method="post" action="send-command.php">
         <?php print $_SERVER['PHP_AUTH_USER']; ?>: <input type="text" autocomplete="off" id="command" name="command" />
	 <input type="submit" value="Send" />
      </form>
   </div>

</body>
</html>
