<?php
session_start();
include 'settings.php';

// Create connection
$db_conn = pg_connect(" host = $hostname port = $port dbname = $dbname user = $username password = $pass ") or die ("Could not connect to server \n");
if (!$db_conn){
	echo "Error: Unable to open database\n:";
}
else
{
	$email = strtolower($_POST['email']);
	$password = $_POST['password'];
	$hashedpass = password_hash($password, PASSWORD_DEFAULT);
	$query = "SELECT id, password, typeid, active FROM adminusers WHERE email = '".$email."'";
	$result = pg_query($db_conn, $query);
	
	while ($row = pg_fetch_row($result))
	{
		$userid = $row[0];
		$dbpass = $row[1];
		$usertype = $row[2];
		$active = $row[3];
	}
	if ($active == 0)
	{
		echo '<script type="text/javascript">';
		echo 'if (confirm("User does not exist or is not active")){document.location="index.php"}';
		echo '</script>';
	}
	else if (($dbpass == $password) || ($hashedpass == $dbpass))
	{	
		$_SESSION['user'] = $userid;
		header("Location: mainpage.php");
	}
	else
	{
		echo '<script type="text/javascript">';
		echo 'if (confirm("Wrong Username or Password")){document.location="index.php"}';
		echo '</script>';
	}
}
pg_close($db_conn);
//header("Location: mainpage.php");
?>
