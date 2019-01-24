<?php
    if(isset($_POST['submit']))
    {
     
     if(getimagesize($_FILES['image']['tmp_name'])==FALSE)
     {
        echo " error ";
     }
     else
     {	
        
        $user = "7349478887";
        $text = $_POST["caption"];
        $category = $_POST["category"];
        $image = $_FILES['image']['tmp_name'];
        $image = addslashes(file_get_contents($image));
        saveimage($image,$text,$category,$user);
        
     }
    }
    function saveimage($image,$text,$category,$user)
    {
        
        $dbcon=mysqli_connect('localhost','root','','selfieless');
        $qry="insert into images (name,caption,category,user) values ('$image','$text',$category,$user)";
        $result=mysqli_query($dbcon,$qry);
        
        
        if($result)
        {
            echo " <br/>Image uploaded.";
            header('location:user-dashboard.html');
        }
        else
        {
            echo " error ";
        }
    }
    
?>
