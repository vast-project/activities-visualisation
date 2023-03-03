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
		$savesubmit=$_POST['savesubmit'];
		if ($savesubmit == 'addevent')
		{
			$datetime = $_POST['date'].' '.$_POST['time'];
			$visitor = $_POST['name'];
			$noofvisitors = $_POST['noofvisitors'];
			$educationlevel = $_POST['educlevel'];
			$query = "INSERT INTO events(datetime, visitor, noofvisitors, educationlevel) VALUES ('".$datetime."','".$visitor."','".$noofvisitors."','".$educationlevel."')";
			$result = pg_query($db_conn, $query);
			$row = pg_fetch_row($result);
			header("Location: mainpage.php");
		}
		else if ($savesubmit == 'back')
		{
			header("Location: mainpage.php");
		}
	}
?>