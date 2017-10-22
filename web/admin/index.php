<html>
<head>
   <title>redmew: Factorio Server Control</title>
   <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
   <link rel="stylesheet" type="text/css" href="factorio.css">
   <link rel="stylesheet" type="text/css" href="redmew.css">
</head>
<body>
   <h1>redmew: Factorio Server Control</h1>

   <div id="serverControl">
      <h2>Server Command and Control</h2>
      <p>Todo - Convert to async JS call, send output to a div</p>
      <ul>
         <li><a href="command.php?cmd=start" class="btn btn-custom btn-large btn-block">Start</a></li>
         <li><a href="command.php?cmd=stop" class="btn btn-custom btn-large btn-block">Stop</a></li>
         <li><a href="command.php?cmd=restart" class="btn btn-custom btn-large btn-block">Restart</a></li>
         <li><a href="command.php?cmd=update" class="btn btn-custom btn-large btn-block">Update</a></li>
         <li><a href="command.php?cmd=save" class="btn btn-custom btn-large btn-block">Save</a></li>
      </ul>
   </div>

   <div id="serverStatus">
      <h2>Server Status</h2>
      <p>Todo - Convert to async JS call, send output to a div</p>
      <iframe src="./status.php" frameBorder="0" height="30"></iframe><br> <br>
   </div>

   <div id="chat">
      <h2>Chat</h2>
      <p>Todo - Convert to async JS call, send output to a div</p>
      <iframe src="./chat.php" height="300" width="600">
   </div>

</body>
</html>
~
