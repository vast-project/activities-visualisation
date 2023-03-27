<!DOCTYPE html>
<html>
<head>
	<title>Activities' Visualization</title>
	<link rel="stylesheet" type="text/css" href="css/style.css">
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@500&display=swap" rel="stylesheet">
</head>
<body>
	<div class="main">  	
		<input type="checkbox" id="chk" aria-hidden="true">

			<div class="login">
				<form action="login.php" method="post">
					<img src="media/VAST_LOGO.jpg"/>
					<label for="chk" aria-hidden="true">WELCOME TO VAST - ACTIVITIES' VISUALIZATION SITE</label>
					<input type="email" name="email" placeholder="Email" required>
					<input type="password" name="password" placeholder="Password" required>
					<button type="submit">Login</button>
					<p>&copy; VAST Project 2023</p>
				</form>
			</div>
			
			<div class="resetpass">
				<form action="resetpassword.php" method="post">
					<label for="chk" aria-hidden="true">Reset Password</label>
					<input type="email" name="email" placeholder="Email" required>
					<button>Reset Password</button>
				</form>
				
			</div>
	</div>
</body>
</html>