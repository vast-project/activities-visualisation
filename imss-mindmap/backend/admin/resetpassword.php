<?php
	include 'db_connect.php';
	require("/usr/share/php/PHPMailer/src/PHPMailer.php");
	require("/usr/share/php/PHPMailer/src/SMTP.php");
	require("/usr/share/php/PHPMailer/src/Exception.php");
	
	// Create connection
	$db_conn = mysqli_connect("host = $hostname port = $port dbname = $dbname user = $username password = $pass ") or die ("Could not connect to server \n");

	if (!$db_conn){
		echo "Error: Unable to open database\n:";
	}
	else
	{
		$email = $_POST['email'];
		$token="";
		$query = "SELECT * FROM users WHERE email = '$email'";
		$result = mysqli_query($db_conn, $query);
		while ($row = mysqli_fetch_row($result))
		{
			$emailId = $row[0];
			$token = md5($email).rand(10,9999);
			//if ($token=="")
			//{
			//	echo "Invalid Email Address. Go back";
			//}
			$expFormat = mktime(date("H"), date("i"), date("s"), date("m") ,date("d")+1, date("Y"));
			$expDate = date("Y-m-d H:i:s",$expFormat);
			$query = "UPDATE users SET resetlinktoken='" . $token . "' ,expdate='" . $expDate . "' WHERE email='" . $email . "'";
			$result = mysqli_query($db_conn, $query);
			$link = "<a href='http://".$hostname."/distributors/reset-password-form.php?key=".$emailId."&token=".$token."'>Click To Reset password</a>";

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
			$mail->AddAddress($email, $row[2]);
			//$mail->AddAddress('reciever_email_id', 'reciever_name');
			$mail->Subject  =  'Reset Password';
			$mail->IsHTML(true);
			$mail->Body = 'Click On This Link to Reset Password '.$link;

			if($mail->Send())
			{
			  echo "Check Your Email and Click on the link sent to your email";
			}
			else
			{
			  echo "Mail Error - >".$mail->ErrorInfo;
			}
		}
		header("Location: index.html");
	}
?>
