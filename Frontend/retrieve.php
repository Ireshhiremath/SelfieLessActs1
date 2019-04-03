<?php

    
    $connect = mysqli_connect("localhost", "root", "", "selfieless"); 
     
                $query = "SELECT i.name, i.caption from images as i where user ='7349478887'";  
                $result = mysqli_query($connect, $query);  
                while($row = mysqli_fetch_array($result))  
                {  
                     echo '  
                          <tr>  
                               <td>  
                                    <img src="data:image/jpeg;base64,'.base64_encode($row['name'] ).'" height="200" width="200" class="img-thumnail" />  
                               </td>  
                          </tr>  
                     ';  
                }  
              

?>
