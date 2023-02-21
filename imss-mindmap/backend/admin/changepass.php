<?php
session_start();
include 'db_connect.php';
$db_conn = mysqli_connect(" host = $hostname port = $port dbname = $dbname user = $username password = $pass ") or die ("Could not connect to server \n");
?>
<!DOCTYPE html>
<html>
<head>
	<title>Intelligo Free Distributors' Area</title>
	<link rel="stylesheet" type="text/css" href="css/complaint_style.css">
	<link href="https://fonts.googleapis.com/css2?family=Jost:wght@500&display=swap" rel="stylesheet">
</head>
<body>
	<div class="main" style="width:50%;">
		<table width="95%">
			<tr>
				<td align ="left" style="width:80%;">
					<label>Welcome user: 
						<?php 
						if (!$db_conn){
							echo "Error: Unable to open database\n:";
						}
						else
						{
							$query = "SELECT id, fullname FROM users WHERE id = ". $_SESSION['user'];
							$result = mysqli_query($db_conn, $query);
							$row = mysqli_fetch_row($result);
							echo $row[1];
						}
						?>
					</label>
				</td>
				<td align ="right" style="width:20%;">
					<form action="logout.php" method="post" align ="right">
						<button type="submit" class="logoutbtn" align ="right">Logout</button>
					</form>
				</td>
			</tr>
		</table>
		<br>
		<form action="changepasstodb.php" method="post">			
			<table width="95%">
				<tr >
					<th colspan="4">Change your password</th>
				</tr>
				<tr>
					<td style="width:25%;"><label>Enter Your Old Password:</label></td><!--id="psw" name="psw"-->
					<td style="width:75%;"><input type="password" name="oldpass" id="oldpass" placeholder="Enter Your Old Password" required></td>
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
			</table>
			<input type="hidden"  $row[0]>
			<button id="btnchangepass" type="submit" name="currentuser" value="<?php echo $row[0]; ?>">Change your Password</button>
		</form>
		<br>
	</div>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script type="text/javascript">
		$('#btnchangepass').attr("disabled", true);
		$('#newpass, #confirmpass').on('keyup', function () {
			if ($('#newpass').val() == $('#confirmpass').val()) {
				$('#btnchangepass').attr("disabled", false);
			}
			else {
				$('#btnchangepass').attr("disabled", true);
			}
		});
	</script>
</body>
</html>