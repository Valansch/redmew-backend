<html>
<head>
<?php
        $cmd = $_GET['cmd'];
        if ($cmd == "update") {
                shell_exec('/home/factorio/server/control/update');
        } elseif ($cmd == "start") {
                shell_exec('/home/factorio/server/control/start');
        } elseif ($cmd == "restart") {
                shell_exec('/home/factorio/server/control/restart');
        } elseif ($cmd == "stop") {
                shell_exec('/home/factorio/server/control/stop');
        } elseif ($cmd == "save") {
                shell_exec('tmux send-keys -t live test Enter');
        } if ($_GET['cmd'] != null) {
                header('Location: /admin/');
        }
?>
</head>
<body>
<input type="button" onclick="location.href='/admin/?cmd=start'" value="Start"> <br>
<input type="button" onclick="location.href='/admin/?cmd=stop'" value="Stop"> <br>
<input type="button" onclick="location.href='/admin/?cmd=restart'" value="Restart"> <br>
<input type="button" onclick="location.href='/admin/?cmd=update'" value="Update"> <br>
<input type="button" onclick="location.href='/admin/?cmd=save'" value="Save"> <br>
<iframe src="/admin/status.php" frameBorder="0" height="30"></iframe><br> <br>
<iframe src="/admin/chat.php" height="300" width="600">
</body>
</html>
~
