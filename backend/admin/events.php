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
								$query = "SELECT fullname FROM adminusers WHERE id = ". $_SESSION['user'];
								$result = pg_query($db_conn, $query);
								$row = pg_fetch_row($result);
								echo $row[0];
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
		<form action="eventstodb.php" method="post">
			<table table width="95%">
				<tr>
					<th colspan="2">Add New Event - New Event Details</th>
				</tr>
				<tr>
					<td><label>Visitor's Name</label></td>
					<td><input type="text" name="name" placeholder="Visitor's Name" required></td>
				</tr>
				<tr>
					<td><label>Date / Time of Visit</label></td>
					<td><table width="100%"><tr><td><input type="date" name="date" placeholder="Date/Time" required></td><td>&ensp;</td><td><input type="time" name="time" placeholder="Date/Time" required></td></tr></table></td>
				</tr>
				<tr>
					<td><label>Number of Participants</label></td>
					<td><input type="number" name="noofvisitors" placeholder="Number of Participants" min="1" max="200" required></td>
				</tr>
				<tr>
					<td><label>Education Level of Participants</label></td>
					<td>
						<select name="educlevel" id="educlevel" placeholder="Education Level of Participants" required aria-invalid="false">
							<option value="" selected>--- Select Education Level of Participants ---</option>
							<?php
								if (!$db_conn){
									echo "Error: Unable to open database\n:";
								}
								else
								{
									$query = "SELECT id, level FROM educationlevel ORDER BY level asc";
									$result = pg_query($db_conn, $query);
									while ($row = pg_fetch_row($result))
									{
										echo ('<option value="');
										echo $row[0];
										echo ('">');
										echo $row[1];
										echo ('</option>\n');
									}
								}
							?>
						</select>
					</td>
				</tr>
				<tr>
					<td><button type="submit" name="savesubmit" value="addevent" >Add Event</button></td>
					<td><button type="submit" name="savesubmit" value="back" formnovalidate="formnovalidate">Cancel</button></td>
				</tr>
			</table>
		</form>
	</div>
</body>
</html>