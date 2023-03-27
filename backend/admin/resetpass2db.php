<?php
	session_start();
	include 'db_connect.php';
	require("/usr/share/php/PHPMailer/src/PHPMailer.php");
	require("/usr/share/php/PHPMailer/src/SMTP.php");
	require("/usr/share/php/PHPMailer/src/Exception.php");

	// Create connection
	$db_conn = pg_connect(" host = $hostname port = $port dbname = $dbname user = $username password = $pass ") or die ("Could not connect to server \n");

	if (!$db_conn){
		echo "Error: Unable to open database\n:";
	}
	else
	{
		$userid = $_POST['email'];
		$password = $_POST['newpass'];
		$curdate = date("Y-m-d");
		$query = "SELECT password, email, companyid from public.users WHERE id= ".$userid.";";
		$result = pg_query($db_conn, $query);
		$row = pg_fetch_row($result);
		$email=$row[1];
		$companyid = $row['2'];
		$hashedpass = password_hash($password, PASSWORD_DEFAULT);
		$query = "UPDATE public.users SET password= $$".$password."$$, active=1, termsdate='".$curdate."', termsrev='1', resetlinktoken='' WHERE id= ".$userid.";";
		$result = pg_query($db_conn, $query);

		if (pg_affected_rows($result) >= 1){
			$query = "SELECT name, countryid from public.distributors WHERE id= ".$companyid.";";
			$result = pg_query($db_conn, $query);
			$row = pg_fetch_row($result);
			$companyname=$row['0'];
			$companycountry=$row['1'];
			$query = "SELECT name from public.countrycodes WHERE id= ".$companycountry.";";
			$result = pg_query($db_conn, $query);
			$row = pg_fetch_row($result);
			$companycountry=$row['0'];
			$mail = new PHPMailer\PHPMailer\PHPMailer();
			$mail->CharSet =  'utf-8';
			$mail->IsSMTP();
			//$mail->SMTPDebug = 1;
			// enable SMTP authentication
			$mail->SMTPAuth = true;                  
			// mail username
			$mail->Username = 'ch.damianou@hemoglobe15.com';
			// mail password
			$mail->Password = 'Drukflm558!!';
			$mail->SMTPSecure = 'SSL'; 
			$mail->SMTPAuth = true;			
			$mail->Host = 'mail.hemoglobe15.com';
			// set the SMTP port for the mail server
			$mail->Port = '587';
			$mail->From='ch.damianou@hemoglobe15.com';
			$mail->FromName='Intelligo BV';
			$mail->AddAddress('regulatory@intelligofree.com', 'Regulatory');
			//$mail->AddAddress('reciever_email_id', 'reciever_name');
			$mail->addAttachment('media/I-FO-5.3-003_2_Intelligo Privacy Policy.pdf');
			$mail->Subject  =  "Confirmation – the distributor has signed the terms & conditions / policy";
			$mail->IsHTML(true);
			$mail->Body = "User from Distributor  ".$companyname." (".$companycountry.")  has signed the terms & conditions on date ".$curdate."
			<br>User: ".$email." just accepted Terms and Conditions.";

			if($mail->Send())
			{
				echo "<script>alert('Password changed successfully'); window.location.href='index.html';</script>";
			}
			else
			{
			  echo "Mail Error - >".$mail->ErrorInfo;
			}

			
		}
		else {
			//echo "<script>alert('Password has NOT been changed'); window.location.href='select_action_user.php';</script>";

			echo "<script>alert('Password has NOT been changed');</script>";
		}
	}
?>