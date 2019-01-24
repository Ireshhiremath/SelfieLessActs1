
<?php
    
       $db = mysqli_connect("localhost","root","","selfieless"); 
$sql = "SELECT * FROM images";
$sth = $db->query($sql);
$result=mysqli_fetch_array($sth);
echo '<img src="data:image/jpeg;base64,'.base64_encode( $result['image'] ).'"/>';


?>

