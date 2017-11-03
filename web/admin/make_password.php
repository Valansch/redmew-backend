<head>
<script>
	function redirect() {
		var URL = window.location + "?password=" + document.getElementById("pw").value;
		window.location.replace(URL);
	}
</script>
</head>
<?php
if ($_GET['password'] != null) {
	var_dump(password_hash($_GET['password'], PASSWORD_DEFAULT));
} else {
	echo('Password: <input type="input" id="pw"/>	<input type="submit" onclick="redirect()" />');
}
