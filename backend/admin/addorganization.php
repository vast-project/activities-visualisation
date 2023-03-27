<?php
session_start();
include 'settings.php';
$db_conn = pg_connect(" host = $hostname port = $port dbname = $dbname user = $username password = $pass ") or die ("Could not connect to server \n");
?>
<!DOCTYPE html>
<html>
<head>
	<title>Activities' Visualization Admin Panel</title>
	<link rel="stylesheet" type="text/css" href="css/sortable-table.css">
	<link rel="stylesheet" type="text/css" href="css/menu_css.css">
	<link href="https://fonts.googleapis.com/css2?family=Jost:wght@500&display=swap" rel="stylesheet">
</head>

<body>
	<div class="main">  	
		<div>
			<table>
				<tr>
					<td align ="left" style="width:80%;">
						<label>Welcome user: 
							<?php 
							if (!$db_conn){
								echo "Error: Unable to open database\n:";
							}
							else
							{
								$query = "SELECT fullname, typeid FROM adminusers WHERE id = ". $_SESSION['user'];
								$result = pg_query($db_conn, $query);
								$row = pg_fetch_row($result);
								echo $row[0];
								$usertype = $row[1];
							}
							?>
						</label>
					</td>
					<td align ="right" style="width:20%;">
						<form action="changepass.php" method="post" align ="right">
							<button type="submit" class="logoutbtn" align ="right">Change password</button>
						</form>
					</td>
					<td align ="right" style="width:20%;">
						<form action="logout.php" method="post" align ="right">
							<button type="submit" class="logoutbtn" align ="right">Logout</button>
						</form>
					</td>
				</tr>
			</table>
		</div>
		<form action="addorgtodb.php" method="post">
			<table table width="95%">
				<tr>
					<th colspan="2">Add New Organization</th>
				</tr>
				<tr>
					<td><label>Organization Name</label></td>
					<td><input type="text" name="orgname" placeholder="Organization Name" required></td>
				</tr>
                <tr>
					<td><label>Organization Phone</label></td>
					<td><input type="text" name="orgphone" placeholder="Organization Phone Number"></td>
				</tr>
                <tr>
					<td><label>Organization Address</label></td>
					<td><input type="text" name="orgaddress" placeholder="Organization Address"></td>
				</tr>
				<tr>
					<td><button type="submit" name="savesubmit" value="addorganization">Add Organization</button></td>
					<td><button type="submit" name="savesubmit" value="back" formnovalidate="formnovalidate">Cancel</button></td>
				</tr>
			</table>
		</form>
	</div>
</body>
</html>