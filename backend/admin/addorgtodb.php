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
		if ($savesubmit == 'addorganization')
		{
			$name = $_POST['orgname'];
			$phone = $_POST['orgphone'];
			$address = $_POST['orgaddress'];
			
			$query = "INSERT INTO organizations (name";
			if ($phone!='') {$query = $query . ", phone ";}
			if ($address!='') {$query = $query . ", address ";}
			$query = $query . ") VALUES ('".$name."'";
			if ($phone!='') {$query = $query . ", " .$phone;}
			if ($address!='') {$query = $query . ", '" .$address. "'";}
			$query = $query . ")";
			$result = pg_query($db_conn, $query);
			$row = pg_fetch_row($result);
			header("Location: organizations.php");
		}
		else if ($savesubmit == 'back')
		{
			header("Location: organizations.php");
		}
	}
?>