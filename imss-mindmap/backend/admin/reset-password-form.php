<?php
	include 'db_connect.php';
	$db_conn = mysqli_connect(" host = $hostname port = $port dbname = $dbname user = $username password = $pass ") or die ("Could not connect to server \n");
?>
<!doctype html>
<html>
<head>
	<title>Intelligo Free Distributors' Area</title>
	<link rel="stylesheet" type="text/css" href="css/complaint_style.css">
	<link href="https://fonts.googleapis.com/css2?family=Jost:wght@500&display=swap" rel="stylesheet">
</head>
<body>
<div class="main" style="width:50%;">
<?php
if($_GET['key'] && $_GET['token'])
{
	$email = $_GET['key'];
	$token = $_GET['token'];
	$query = "SELECT * FROM users WHERE resetlinktoken='".$token."' and id='".$email."';";
	$result = mysqli_query($db_conn, $query);
	$curDate = date("Y-m-d H:i:s");
	if (mysqli_num_rows($result) > 0) {
		$row = mysqli_fetch_array($result);
		//if(($row['expdate'] >= $curDate)||($row['expdate'] =='')){ 
			echo '<form action="resetpass2db.php" method="post">			
			<table width="95%">
				<tr >
					<th colspan="4">Change your password</th>
				</tr>
				<tr>
					<td style="width:25%;"><label>Enter New Password:</label></td><!--id="psw" name="psw"-->
					<td style="width:75%;"><input type="password" name="newpass" id="newpass" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" placeholder="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters" required></td>
				</tr>
				<tr>
					<td style="width:25%;"><label>Re-enter Password:</label></td>
					<td style="width:75%;"><input type="password" name="confirmpass" id="confirmpass" placeholder="Re-Enter your new Password" required></td>
				</tr>
				<tr><td colspan="2">REMINDER: Password must contain at least one number, one uppercase and one lowercase letter, and at least 8 characters</td></tr>
				<tr>
					<td><input type="checkbox" name="terms" id="terms" required></td>
					<td colspan="3"><label>I have read and accept  <a href="terms.html" target="blank">Terms and Conditions</a>  (*)</label></td>
				</tr>
			</table>
			<input type="hidden" name="email" id="email" value="'.$row[0].'">
			<button id="btnchangepass" type="submit" name="currentuser" value="<?php echo $row[0]; ?>">Change your Password</button>
		</form>';
		//}
		//else
		//{
		//	echo '<p>This forget password link has been expired</p>';
		//}
	}
}
?>
</div>
</body>
</html>
