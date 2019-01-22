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
		$number=$_POST["phone"];
		
		$password=$_POST["cpwd"];
	  if($_POST["pwd"]!=$_POST["cpwd"])
		{
			//  echo "password not matching enter properly";
			 include "signup.html";
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
			$query="SELECT * FROM USER";
			$res=mysqli_query($conn,$query);
			$flag=0;
			while($row=mysqli_fetch_assoc($res))
			{
				if($row['pho_num']==$number)
				{
					$flag=1;
				}
			}
			if($flag==1)
			{
				include "signup.html";
				?>
				<html>
				<body>
					<script>
					alert("User Already exist, you can login now.");
					</script>
				</body>
			</html>
			<?php
			}
			else
			{
					$query="INSERT INTO USER VALUES ('$number','$password')";
                    
                    $res=mysqli_query($conn,$query);
					if(!$res)
					{?>
                                                <script>
                        alert("Not updated.");
                        </script>
                        <?php
						 include "signup.html";
					}
					else
					{
                        ?>
                        <html>
                            <body>
                                <h2><?php echo $number ?></h2>
                                <h2><?php echo $password ?></h2>
                    </body>
                    </html>

                        <script>
                        alert(" updated.");
                        </script><?php
					
						 //include "user-dashboard.html";
					}
			 }
		 }
	 }
?>
