<?php
	session_start();
	include 'settings.php';
	
	// Create connection
	$db_conn = mysqli_connect($hostname, $username, $pass, $dbname) or die ("Could not connect to server \n".mysqli_connect_error());
	
	if (!$db_conn){
		echo "Error: Unable to open database\n:";
	}
	else
	{
		echo "234erwdsf";
		$id = $_POST['changeactiveuser'];
		$query = "SELECT active FROM adminusers WHERE id='".$id."'";
		$result = mysqli_query($db_conn, $query);
		$row = mysqli_fetch_row($result);
		if ($row[0]==1)	{		
			$query = "UPDATE `adminusers` SET active='0' WHERE id='".$id."'";
		}
		else
		{
			$query = "UPDATE `adminusers` SET active='1' WHERE id='".$id."'";
		}
		echo $query;
		$result = mysqli_query($db_conn, $query);
		$row = mysqli_fetch_row($result);
		header("Location: users.php");
	}
?>