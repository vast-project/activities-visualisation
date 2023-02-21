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
		$savesubmit=$_POST['savesubmit'];
		if ($savesubmit == 'adduser')
		{
			$fullname = $_POST['date'].' '.$_POST['fullname'];
			$email = $_POST['email'];
			$phone = $_POST['phone'];
			$organization = $_POST['organization'];
			if ($organization==1) {$typeid=1;} else {$typeid=2;}
			
			$query = "INSERT INTO `adminusers`(`email`, `password`, `organization`, `active`, `fullname`, `phone`, `typeid`) 
									VALUES ('.$email.','Abc@123456','".$organization."','0','".$fullname."','".$phone."','".$typeid."')";
			$result = mysqli_query($db_conn, $query);
			$row = mysqli_fetch_row($result);
			header("Location: users.php");
		}
		else if ($savesubmit == 'back')
		{
			header("Location: users.php");
		}
	}
?>