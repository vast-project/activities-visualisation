<?php
	session_start();
	include 'settings.php';
	
$db_conn = mysqli_connect($hostname, $username, $pass, $dbname) or die ("Could not connect to server \n".mysqli_connect_error());
	if (!$db_conn){
		echo "Error: Unable to open database\n:";
	}
	else
	{
		$eventid=$_POST['eventid'];
		$query = "SELECT * FROM events WHERE id=".$eventid;
		$result = mysqli_query($db_conn, $query);
		$row = mysqli_fetch_row($result);
		$variables = "id=".$row[0]."'datetime=".$row[1]."'visitor=".$row[2]."'noofparticipants=".$row[3]."'educationlevel=".$row[4];
		
		header("Content-type: application/vnd.ms-word");
		header("Content-Disposition: attachment;Filename=QR_Code_for_Event.doc");
		echo "<html>";
		echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">";
		echo "<body>";
		echo "<h3>QR Code for Event on ".$row[1]."</h3><br>Visitor: ".$row[2]."<br><br>";
		//echo '<img src="https://chart.googleapis.com/chart?chs=500x500&cht=qr&chl=http://www.chdamianou.eu/XXX.php?variables='.$variables.'&choe=UTF-8" width="200" height="200">';
		echo '<img src="https://chart.googleapis.com/chart?chs=500x500&cht=qr&chl='.$mapurl.'?variables='.$variables.'&choe=UTF-8" width="200" height="200">';
		echo "</body></html>";
	}
