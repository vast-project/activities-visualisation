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
			<br> 	
			<table width="95%">
				
				<tr>					
					<?php
					if ($usertype==1) {
					echo '<tr>
					<th colspan="4">Activities Visualization Menu</th>
				</tr>
				<td><label>Select action:</label></td>
					<td>
						<form action="users.php" method="post">
							<button type="submit">Users Managment</button>
						</form>
					</td>
					<td>
						<form action="organizations.php" method="post">
							<button type="submit">Organizations Managment</button>
						</form>
					</td>
					<td>
						<form action="viewdbdata.php" method="post">
							<button type="submit">View Data from Activities</button>
						</form>
					</td>
					<td>
						<form action="undercon.php" method="post">
							<button type="submit">Reports</button>
						</form>
					</td>';
					}
					else {
					echo '<tr>
					<th colspan="2">Activities Visualization Menu</th>
				</tr>
				<td><label>Select action:</label></td>
					<td>
						<form action="events.php" method="post">
							<button type="submit">Add new Event</button>
						</form>
					</td>
					<td>
						<form action="users.php" method="post">
							<button type="submit">Add new User</button>
						</form>
					</td>';
					}
					?>
				</tr>
			</table>
			<br>
		</div>
		<br>
		<?php
		if ($usertype!=1){
		echo'
		<div id="review" class="w3-container city">
			<div class="tablediv">
				<table id="cases" width="95%" align="center" border="1" class="sortable">
					<thead>
						<tr>
							<th colspan="5">Upcoming Events</th>
						</tr>
						<tr>
							<th>Event ID</th>
							<th>Date/TIme of Visit</th>
							<th>Visitor</th>
							<th>Education Level</th>
							<th>&nbsp;</th>
						</tr>
					</thead>
					<tbody>';
							if (!$db_conn){
								echo "Error: Unable to open database\n:";
							}
							else
							{
								$query = "SELECT events.id, datetime,visitor,noofvisitors,educationlevel.level FROM events INNER JOIN educationlevel ON educationlevel.id=events.educationlevel ORDER BY datetime asc";
								$result = pg_query($db_conn, $query);
								if (pg_num_rows($result)==0) { echo ('<tr><td colspan="5">No Data Available</td></tr>'); }
								while ($row = pg_fetch_row($result))
								{
									echo ('<tr><td>');
									echo $row[0];
									echo ('</td><td>');
									echo $row[1];
									echo ('</td><td>');
									echo $row[2];
									echo ('</td><td>');
									echo $row[4];
									echo ('</td><td><form action="downloadevent.php" method="post"><input type="hidden" id="eventid" name="eventid" value="'.$row[0].'"><button type="submit">Download Event Details</button></form></td></tr>');
								}
							}
					echo '</body>
				</table>
			</div>
		</div>';
		}
		?>

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script type="text/javascript">
		setInterval(function(){
			$.post('refresh_session.php');
		},600000); //refreshes the session every 10 minutes
	</script>
</body>
</html>