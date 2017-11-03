<?php
if ($_POST['password'] != null and ($_POST['user'] != null)) {
	echo($_POST['user']);
	echo(password_hash($_POST['password'], PASSWORD_DEFAULT));
} else {
?>
	<form method="post">
	Username:
		<input type="input" name="user"/>
	Password: <input type="input" name="password"/>
		<input type="submit"/>
	</form>
<?php } ?>

