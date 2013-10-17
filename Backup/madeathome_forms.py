form_signup="""
<form method="post">
<link rel="stylesheet" type="text/css" href="signup_style.css">
	<h1> Registration form </h1>
	<br>
	<label> 
	<div> First name </div>
	<input type="text" name="first_name" value=%(first_name_value)s> 
	</label>
	<div style="color: red">%(error_first_name)s</div>
	<br>	
	<label> 
	<div> Last name </div>
	<input type="text" name="last_name" value=%(last_name_value)s> 
	</label>
	<div style="color: red">%(error_last_name)s</div>
	<br>	
	<label> 
	<label> 
	<div> Address </div>
	<input type="text" name="postal_address" value=%(postal_address_value)s> 
	</label>
	<div style="color: red">%(error_postal_address)s</div>
	<br>	
	<div> User name </div>
	<input type="text" name="username" value=%(username_value)s> 
	</label>
	<div style="color: red">%(error_username)s</div>
	<br>	
	<label>	
	<div>Password </div>
	<input type="password" name="password"> 
	</label>
	<div style="color: red">%(error_password)s</div>
	<br>
	<label>
	<div> Verify your password </div>
	<input type="password" name="verify"> 
	</label>
	<div style="color: red">%(error_password_verify)s</div>
	<br>
	<label> 
	<div> Email (optional) </div>
	<input type="text" name="email" value=%(email_value)s> 
	</label>
	<div style="color: red">%(error_email)s</div>
	<br>
	
	<input type="submit">
</form>
"""



#==================LOGIN FORM=======================
form_login="""
<form method="post">
<style type="text/css">
    body{
      font-family:sans-serif;
      width: 800px;
      font-size:20;
      margin: 0 auto;
      padding: 10px;
    }
    label{
      display: block;
      font-size:20px;
      }
      input[type=text]{
          width:400px;
          font-size:20px;
          padding:2px;          
      }
      input[type=password]{
          width:400px;
          font-size:20px;
          padding:2px;          
      }
      textarea{
          width:400px;
          height:300px;
          font-size:17px;
          font-family:monospace;
          }
       input[type=submit]{
          font-size:20;
       }
       .post-heading{
           position: relative;
           border-bottom: 4px solid #666;
           }

    </style>
    
	<h1> Login to your account</h1>
	<br>

	<label> 
	<div> Username </div>
	<input type="text" name="username" value=%(username_value)s> 
	</label>
	<div style="color: red">%(error_username)s</div>
	<br>	
	<label>	
	<div> Password </div>
	<input type="password" name="password"> 
	</label>
	<div style="color: red">%(error_password)s</div>
	<br>
	<input type="checkbox" name="remember_me_box" %(check_box_val)s> Remember me!
	
	<br>
	<br>
	<input type="submit">
</form>
"""
