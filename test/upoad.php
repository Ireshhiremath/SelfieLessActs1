<html>
<body>
<form method="post" >
<input type="file" name="image"/>
<input type="submit" name="submit" value="Upload"/>
</form>
<?php
    if(isset($_POST['submit']))
    {
     if(getimagesize($_FILES['image']['tmp_name'])==FALSE)
     {
        echo " error ";
     }
     else
     {	
	$text = "This is a testing process.Here the images will be uploaded to database for 
			 further work";
        $image = $_FILES['image']['tmp_name'];
        $image = addslashes(file_get_contents($image));
        saveimage($image,$text);
     }
    }
    function saveimage($image,$text)
    {
        $dbcon=mysqli_connect('localhost','root','','selfieless');
        $qry="insert into imagefile (name,caption1) values ('$image','$text')";
        $result=mysqli_query($dbcon,$qry);
        if($result)
        {
            echo " <br/>Image uploaded.";
            header('location:../user-dashboard.html');
        }
        else
        {
            echo " error ";
        }
    }
?>
</body>
</html>
