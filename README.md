# Project3

### i. The IP address and SSH port
***IP:***	18.195.120.209 \
***Port:*** 2200 


### ii. The complete URL to your hosted web application.

http://tkazatelgames.tk/ \
if above is not working \
http://18.195.120.209/ 


### iii. A summary of software you installed and configuration changes made.


***
###### User Management 1 - Can you log into the server as the user grader using the submitted key?

1) create user grader\
```sudo adduser grader```
2) check existing user file\
```sudo ls /etc/sudoers.d/```
	> 90-cloud-init-users  README
	
###### User Management 3 - Is the grader user given sudo access?

3) copy existing file and then edit it \
   ```sudo cp /etc/sudoers.d/90-cloud-init-users /etc/sudoers.d/grader```
    
   ``` sudo vi /etc/sudoers.d/grader```\
   Replace ubuntu user with grader by vi type as below\
    	:%s/ubuntu/grader/ \
    Verify configuration\
    ```sudo cat /etc/sudoers.d/grader```
###### User Management 1 - Can you log into the server as the user grader using the submitted key?

4) Change user to grader\
```su - grader```\
    Veriffy sudo rights, by root accesdible folder\
    ```sudo ls /etc/sudoers.d/```

5) Generate RSA key for user grader \
```ssh-keygen```\
```ls -l .ssh/```\
Rename public key\
```mv .ssh/id_rsa.pub .ssh/authorized_keys```\
Set permissions\
```chmod 700 .ssh```\
```chmod 644 .ssh/authorized_keys```

###### User Management 2 - Is remote login of the root user disabled?

6) Disable root remote acccess \
sudo vi /etc/ssh/sshd_config \
```	#PermitRootLogin prohibit-password```\
```	PermitRootLogin no```

###### Security 3 - Are the applications up-to-date?

7) update and upgrade\
```sudo apt-get update```\	
```sudo apt-get upgrade```	

###### Security 2 - Are users required to authenticate using RSA keys?  #have been set by default

8) Force RSA key authetification\
    sudo vi /etc/shh/sshd_config\
```	PasswordAuthentication no```
	
	

###### Security 4 - Is SSH hosted on non-default port?


9) allow ports on AWS\
https://lightsail.aws.amazon.com/ls/webapp/eu-central-1/instances/ubuntu-udacity-catalog1/networking\
add new port to lightsail firewall =>  \
Application = Custom, Protocol = TCP, Port = 2200\
Application = Custom, Protocol = TCP, Port = 123

10) change default port for SSH\
sudo vi /etc/ssh/sshd_config\
```	#Port 22```\
```	Port 2200```\
Restart ssh service\
```sudo service ssh restart```\

###### Security 1 - Is the firewall configured to only allow for SSH, HTTP, and NTP?

11) Setup firewall policy , enable ports 2200, 80, 123\
    ```
    sudo ufw status
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow 2200/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 123/tcp
    sudo ufw enable 
    sudo ufw status
    ```

###### Application Functionality 1 - Is there a web server running on port 80?

11) install apache server\
```sudo apt-get install apache2```\
check apache conf\
```sudo cat /etc/apache2/apache2.conf```\
```sudo vi /etc/apache2/ports.conf```   # pot 80 already in use\
```sudo /etc/init.d/apache2 start```

###### Application Functionality 2 - Has the database server been configured to properly serve data?

12) install postgresql with components\
```sudo apt-get install postgresql postgresql-contrib libpq-dev```\
    only local access to DB is allowed
    ```
    sudo vi /etc/postgresql/9.5/main/pg_hba.conf		#only local is allowed by default
	local   all             postgres                                peer
	local   all             all                                     peer
	host    all             all             127.0.0.1/32            md5
	host    all             all             ::1/128                 md5
    ```
    
13) Start DB service\
```sudo service postgresql start```

14) Configure db\
Change user and access DB CLI
    ```
    $ sudo -u postgres -i
    $ psql
    ```
    Inside db CLI
    ```
    CREATE USER catalog WITH PASSWORD grader;
    ALTER USER catalog CREATEDB;
    CREATE DATABASE catalog WITH OWNER catalog;
    Connect to database $ 
    \c catalog
    REVOKE ALL ON SCHEMA public FROM public;
    GRANT ALL ON SCHEMA public TO catalog;
    ```


######  Application Functionality 3 - Has the web server been configured to serve the Item Catalog application?

15) Install wsgi app\
```sudo apt-get install libapache2-mod-wsgi python-dev```\
    enable wsgi\
```sudo a2enmod wsgi```

16) Setup virtual env for python
    ```
    sudo apt-get install python-pip
    sudo pip install virtualenv
    sudo virtualenv venv
    source venv/bin/activate
    sudo chmod -R 777 venv
    ```
17) Install modules
    ```
    pip install flask
    pip install httplib2
    pip install requests
    pip install sqlalchemy
    pip install oauth2client
    pip install psycopg2
    ```

18) Install catalog app
    ```
    mkdir /var/www/catalog
    sudo chown grader:grader /var/www/catalog
    cd /var/www/catalog
    git clone https://github.com/Kazatel/catalog.git
    ```
19) Configure wsgi app\
sudo vi /var/www/catalog/catalog.wsgi
    ```
    #!/usr/bin/python
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0, "/var/www/catalog/")
    
    from catalog import app as application
    application.secret_key = 'kazatel1'
    ```
20) Configure appache\
sudo vi /etc/apache2/sites-enabled/catalog.conf

    ```
    <VirtualHost *:80>
        ServerName 18.198.120.209
        ServerAlias ec2-13-232-240-16.ap-south-1.compute.amazonaws.com
        ServerAdmin grader@18.198.120.209
        WSGIDaemonProcess catalog python-path=/var/www/catalog:/var/www/catalog/venv/lib/python2.7/site-packages
        WSGIProcessGroup catalog
        WSGIScriptAlias / /var/www/catalog/catalog.wsgi
        <Directory /var/www/catalog/catalog/>
            Order allow,deny
            Allow from all
        </Directory>
        Alias /static /var/www/catalog/catalog/static
        <Directory /var/www/catalog/catalog/static/>
            Order allow,deny
            Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>
    ```

20) create DB teable and load initial data
    ```
    cd /var/www/catalog/catalog
    python database_setup.py
    python lotsofmenus.py
    ```
    
20) create DB teable and load initial data
    ```
    sudo /etc/init.d/apache2 restart
    ```
######  iv. A list of any third-party resources you made use of to complete this project. 

https://www.codementor.io/abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft
https://modwsgi.readthedocs.io/en/develop/user-guides/virtual-environments.html
https://www.postgresql.org/docs/8.0/sql-createuser.html
http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/

