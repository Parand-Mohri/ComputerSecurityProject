# ComputerSecurity
CS 2022 Projects Year 3 Maastricht university Bachelor Data Science and Artificial intelligence.

###Participant:
* B Caissotti di Chiusaño
* Shirley Isabelle Pierre Océane De Koster 
* Mahshid Ghaffari
* Ben Haseñsoñ
* π  Mohri
* Claudia Sañchez Muñoz Cuevas Carmona Lopez Pastor Tarez Marino Gonzalez Delgado 

### Run the client using the read me file in client  

### To run the server
Open the Server folder in command line(Terminal) and run the following command
```
flask run
```
####If there is an error for flask_cors need to go to project interpreter and install flask_cors

###Description 
* Only two legit customer can be in the same account
* Only able to log out from same ip and port that was used for log in 
* If try to log in with wrong password after 3 fail attempts need to wait for 3 minutes
* Need password for login and logout 
* The counter can't be less then -200 or more than 2000000 

### Vulnerabilities found by other groups
* Brute Force Password: No Limit to the number of password attempts 
* The API for logging in returns a “Incorrect Password” response if the password does not match.
* As the user’s password is not verified for logout, users can be logged out simply if the username is unknown.
* No cryptography is used to secure requests so a MITM attack would show the user’s password and username in plain text
* Balance/Counter goes to infinity (denoted in the log as “Inf”) when inputting an extremely large
number.


### Vulnerabilities we found by ourselves
* Accept empy ID and password 

### Vulnerabilities we fixed in fix it part
* Limitation for password attempts (after 3 wrong attempts need to wait for 3 minutes)
* Password for logout 
* Limit on counter 
* Only logout possible from same servers that log in was done
* Not allow making account with empty Id and password 
* No specify error given so attacker dont know if the password is wrong or id (fix second vulnerability given)
* Encrypting the code 
