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
		$id = $_POST['changeactiveuser'];
		$query = "SELECT active FROM adminusers WHERE id='".$id."'";
		$result = pg_query($db_conn, $query);
		$row = pg_fetch_row($result);
		if ($row[0]==1)	{		
			$query = "UPDATE adminusers SET active='0' WHERE id='".$id."'";
		}
		else
		{
			$query = "UPDATE adminusers SET active='1' WHERE id='".$id."'";
		}
		$result = pg_query($db_conn, $query);
		$row = pg_fetch_row($result);
		header("Location: users.php");
	}
?>