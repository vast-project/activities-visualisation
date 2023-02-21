<?php
	session_start();
	include 'db_connect.php';
	
	// Create connection
	$db_conn = mysqli_connect("host = $hostname port = $port dbname = $dbname user = $username password = $pass ") or die ("Could not connect to server \n");

	if (!$db_conn){
		echo "Error: Unable to open database\n:";
	}
	else
	{
		$userid = $_POST['currentuser'];
		$oldpassword = $_POST['oldpass'];
		$password = $_POST['newpass'];
		$hashedoldpass = password_hash($oldpassword, PASSWORD_DEFAULT);
		$query = "SELECT password from public.users WHERE id= ".$userid.";";
		$result = mysqli_query($db_conn, $query);
		$row = mysqli_fetch_row($result);
		if ($oldpassword == $row[0]) {
			$hashedpass = password_hash($password, PASSWORD_DEFAULT);
			$query = "UPDATE public.users SET password= $$".$password."$$ WHERE id= ".$userid.";";
			$result = mysqli_query($db_conn, $query);

			if (mysqli_affected_rows($result) >= 1){
				echo "<script>alert('Password changed successfully'); window.location.href='select_action_user.php';</script>";
			}
			else {
				echo "<script>alert('Password has NOT been changed'); window.location.href='select_action_user.php';</script>";
			}
		}
		else if ($hashedoldpass == $row[0]) {
			$hashedpass = password_hash($password, PASSWORD_DEFAULT);
			$query = "UPDATE public.users SET password= $$".$password."$$ WHERE id= ".$userid.";";
			$result = mysqli_query($db_conn, $query);

			if (mysqli_affected_rows($result) >= 1){
				echo "<script>alert('Password changed successfully'); window.location.href='select_action_user.php';</script>";
			}
			else {
				echo "<script>alert('Password has NOT been changed'); window.location.href='select_action_user.php';</script>";
			}
		}
		else
		{
			echo "<script>alert('Wrong User Password. Password has NOT been changed'); window.location.href='select_action_user.php';</script>";
		}
	}
?>