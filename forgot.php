defr
<?php
	$servername="localhost";
	$username="root";
	$password="";
	$conn=mysqli_connect($servername,$username,$password,"selfieless");
	if(!$conn)
	{
		// echo "connection not established";
	}
	else
	{
		// echo "connection estsblished successfully";
		$NUMBER=$_POST["phone"];
		$PASSWORD=$_POST["pwd"];
		$CPASSWORD=$_POST["cpwd"];
		if($PASSWORD!=$CPASSWORD)
		{
				// echo "entered passwords not matching";
				include "forgot.html";
				?>
				<html>
				<body>
					<script>
					alert("entered passwords not matching");
					</script>
				</body>
			</html>
			<?php

		}
		else
		{
		$query="UPDATE USER SET pass='$PASSWORD' WHERE pho_num='$NUMBER'";
		$res=mysqli_query($conn,$query);

		if(!$res)
		{
			// echo "TRY NEXT TIME";
		}
		else
		{
				// echo "password successfully updated";
				include "user-dashboard.html";
				?>
				<html>
				<body>
					<script>
					alert("password successfully updated");
					</script>
				</body>
			</html>
			<?php

		}

	}
}
?>
